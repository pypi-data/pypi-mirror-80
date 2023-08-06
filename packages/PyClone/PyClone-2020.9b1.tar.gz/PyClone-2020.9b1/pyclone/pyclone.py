#!/usr/bin/env python -u
# -*- coding: utf-8 -*-

# System
import sys
import signal
import time

# Data
import json

# Processes/Threads
import pexpect
import threading

# Types
import collections
import arrow

# Logging
from logbook import Logger
from pyclone.log import logger_group
logger = Logger( __loader__.name )
logger_group.add_logger( logger )

class PyClone( object ):
	'''

	Parameters
	----------
	binPath : :obj:`str`, optional
		Path to rclone binary at either the host level (e.g. ``/usr/bin/env rclone``) or container level (e.g. ``docker-compose --no-ansi --file /path/to/docker-compose.yaml run rclone``)

	messageBufferSize : :obj:`int`, optional
		Maximum number of messages to hold in buffer for pulling out with :any:`PyClone.readline()`.


	.. seealso::

		:any:`PyClone.binPath()` for updating the binary path to rclone after the class has been instantiated.

	'''

	# rclone
	__binPath		=	None				#: Path to Rclone.
	__flags			=	{}					#: Global flags set with :any:`PyClone.addFlag()` and unset with :any:`PyClone.removeFlag()`.

	# Processes
	__proc			=	None				#: `rclone` process spawned with `pexpect`.
	__thread		=	None				#: Thread that starts rclone process and writes to message buffer.

	# Internal
	__messages		=	None				#: Message buffer that is written to by :any:`PyClone.__threadedProcess()` and read by :any:`PyClone.readline()`.
	line			=	None				#: Current line pulled from message buffer with :any:`PyClone.readline()`.
	__lock			=	threading.Lock()	#: Used to avoid simultaneous runs of rclone within a PyClone instance.

	def signalsDict( self, k=None ):
		'''

		Used for looking up a signal by its integer or string value, or a dictionary listing of all available signals.

		Parameters
		----------
		k : :obj:`int` or :obj:`str`, optional

		Returns
		-------
		:obj:`int`, :obj:`str`, or :obj:`dict`
			Returns a dictionary by default, or the desired signal lookup (`string` if an `integer` is given, or `integer` if a `string` is given).

		'''

		d	=	{ str( v ):int( k ) for v,k in signal.__dict__.items() if v.startswith( 'SIG' ) and not v.startswith( 'SIG_' ) }

		if isinstance( k, str ) and k.upper() in d.keys():
			return d[ k ]
			pass # END

		elif isinstance( k, int ) and k in d.values():
			return { v: k for k, v in d.items() }[ k ]
			pass # END

		elif k is None:
			return d
			pass # END

		else:
			return None
			pass # END

		pass # END METHOD : Signals Dictionary

	def sigTrap( self, sigNum, currFrame ):
		'''

		This serves as the process’ signal trap for several default signals (e.g. `SIGINT` and `SIGTERM`).

		While you can override this method, you probably won't ever need to, and can leave this to call upon :any:`PyClone.stop() <PyClone.stop>`.

		Parameters
		----------
		sigNum : :obj:`int`
			Signal number (e.g. `2` for `SIGINT`, or `15` for `SIGTERM`.)

		currFrame : :obj:`frame`
			Python Stack frame.


		.. seealso::

			* :any:`PyClone.signalsDict() <PyClone.signalsDict>` - useful for converting :obj:`sigNum` to a string representation.

		'''

		logger.debug( f'sigTrap() : sigNum={sigNum}, currFrame={currFrame}' )
		self.stop()
		sys.exit()

		pass # END METHOD : Signal trap

	def signals( self, cb, *keys ):
		'''

        Bind a callback to an arbitrary number of signals.

        Parameters
        ----------
        cb : :obj:`Function` or :obj:`Method`
            Callback that's executed when a signal occurs that it's been bound to.

        *keys : :obj:`str`
            Variable length list of signals to bind callback to.

        Returns
        -------
        bool
            `True` if successful, `False` if an error occurs.


        An example for registering a callback to multiple signals:

        .. code-block:: python

            def myCallback( self, sigNum, currFrame ):

                print( f'My callback received sigNum={ sigNum } and currFrame={ currFrame }' )

                pass # END METHOD : My callback

            def __init__( self ):

                self.signals(
                    self.myCallback,
                    'SIGINT',   # ^C
                    'SIGTERM',  # `kill procID` or `pkill myApp.py` and systemd's default kill signal.
                )

                pass # END CONSTRUCTOR

        .. seealso::

            * :any:`PyClone.sigTrap()`

		'''

		r					=	None

		try:

			for currKey in keys:

				currKey	=	currKey.upper()

				if (
					currKey.startswith( 'SIG' )
					and
					not currKey.startswith( 'SIG_' )
					and
					hasattr( signal, currKey )
				):

					sigNum	=	getattr( signal, currKey )
					signal.signal( sigNum, cb )

					logger.debug( f"Signal : bind '{ currKey }' to { cb.__name__ }()." )
					r	=	True

					pass # END IF

				pass # END FOR

			pass # END TRY

		except Exception as e:

			logger.critical( f"{self.name} : {e}" )
			r	=	False

			pass # END EXCEPTION

		finally:

			return r

			pass # END FINALLY

		pass # END METHOD : Signals

	def addFlag( self, key, value=None ):
		'''

		`Rclone` has **many** `global flags <https://rclone.org/flags/>`_ available to every command,
		if a flag doesn't have the option for a value, simply leave it unset.

		**Examples:**

		* Dry run without any changes: ``PyClone.addFlag( 'dry-run' )``

		* Throttling your total bandwidth: ``PyClone.addFlag( 'bwlimit', '10M' )``

		Parameters
		----------
		key : :obj:`str`
		value : :obj:`str`, optional


		.. seealso::

			* :any:`PyClone.updateFlag()` to update a flag.

			* :any:`PyClone.removeFlag()` to remove a flag.

		Returns
		-------
		bool
			`True` if key doesn't exist and has been added, `False` if key already exists and couldn't be added.

		'''

		logger.info( f"Add flag : '{key}'" + ( f" = '{value}'" if value else "" ) + "." )

		# Doesn't exist, add
		if key not in self.__flags:
			self.__flags.update({ key : value })
			return True

		# Exists, don't add
		else:
			return False

		pass # END METHOD : Add flag

	def removeFlag( self, key ):
		'''

		Removes a global flag that was set with :any:`PyClone.addFlag()`

		Parameters
		----------
		key : :obj:`str`


		.. seealso::

			* :any:`PyClone.addFlag()` to add a flag.

			* :any:`PyClone.updateFlag()` to update a flag.


		Returns
		-------
		bool
			`True` if key was found and removed, otherwise `False`.

		'''

		logger.debug( f'removeFlag() : key={key}' )

		if key in self.__flags:
			logger.info( f"Remove flag : '{key}'." )
			del self.__flags[ key ]
			return True
			pass # END IF

		else:
			logger.warning( f'removeFlag() : key not found : {key}' )
			return False
			pass # END ELSE

		pass # END METHOD : Remove flag

	def updateFlag( self, key, value=None ):
		'''

		Overwrites a flag that was set with :any:`PyClone.addFlag()`

		Parameters
		----------
		key : :obj:`str`
		value : :obj:`str`, optional


		.. seealso::

			* :any:`PyClone.addFlag()` to add a flag.

			* :any:`PyClone.removeFlag()` to remove a flag.


		Returns
		-------
		bool
			`True` if :any:`PyClone.removeFlag()` and :any:`PyClone.addFlag()` both returned `True`, otherwise `False`.

		'''

		logger.debug( f'updateFlag() : key={key}, value={value}' )
		return self.removeFlag( key ) and self.addFlag( key, value )

		pass # END METHOD : Update flag

	def __flagsToString( self ):
		'''

		Iterates all flags (and if applicable, values) stored in :any:`PyClone.__flags` with :any:`PyClone.addFlag()` and converts them to command line arguments that are used when spawning the `rclone` process.


		Returns
		-------
		str
			Combination of flags (and where applicable, reciprocal values).

		'''

		r	=	''

		for k, v in self.__flags.items():

			# Add key
			r	+=	f'--{k} '

			# Add value
			if v is not None:
				r	+=	f'{v} '
				pass # END IF

			pass # END FOR

		logger.debug( f'__flagsToString() : return : {r}' )
		return r

		pass # END METHOD : Flags to string options

	def __init__( self, *, binPath=None, messageBufferSize=5 ):
		'''

		Constructor used for initializing an instance of PyClone.

		'''

		# Specified path or fallback to $PATH
		logger.debug( f'__init__() : setting binary path' )
		self.binPath( binPath if binPath else '/usr/bin/env rclone' )

		# Short buffer for Rclone output to dump to, and for Python to pull from.
		logger.debug( f'__init__() : setting __messages with a maximum length of {messageBufferSize}' )
		self.__messages		=	collections.deque( maxlen=messageBufferSize )

		tempSignals			=	[
									'SIGHUP',	# Usually, a reload request.
									'SIGINT',	# ^C
									'SIGQUIT',	# ^\
									'SIGCONT',	# Usually, a resumed process.
									'SIGTERM',	# `kill procID` or `pkill myApp.py` and systemd's default kill signal.
									'SIGTSTP',	# ^Z
								]

		# Catch as many signals as possible.
		logger.debug( f'__init__() : binding signals to sigTrap() : {", ".join( tempSignals )}' )
		self.signals( self.sigTrap, *tempSignals )

		pass # END CONSTRUCTOR : PyClone

	def binPath( self, binPath=None ):
		'''

		Gets (or if a value is provided, sets) path to rclone binary.

		**Examples:**

		* Host: ``/usr/bin/env rclone``

		* Container: ``docker-compose --no-ansi --file /path/to/docker-compose.yaml run rclone``

		Parameters
		----------
		binPath : :obj:`str`, optional
			Path to rclone binary.


		Returns
		-------
		str
			Binary path stored in :any:`PyClone.__binPath()`.

		'''

		logger.debug( f'binPath() : {binPath}' )

		if binPath:
			self.__binPath		=	binPath

		return self.__binPath

		pass # END METHOD : Binary path

	def stop( self ):
		'''

		Used for shutting down rclone (including interrupting transfers, if needed).


		Returns
		-------
		:obj:`tuple` or :obj:`None`
			If a process was successfully spawned, and then successfully shut down with this method, a tuple containing the *exit status* and the *signal status* are returned.

		'''

		# Attempt to close the process before trying to terminate it.
		if hasattr( self.__proc, 'close' ):
			logger.debug( 'stop() : process : close( force=True )' )
			self.__proc.close( force=True )

		# Terminate process
		if hasattr( self.__proc, 'terminate' ):
			logger.debug( 'stop() : process : terminate()' )
			if not self.__proc.terminate():
				logger.debug( 'stop() : process : terminate( force=True )' )
				self.__proc.terminate( force=True )
		pass # END IF

		# Join thread back to main
		if hasattr( self.__thread, 'join' ) and self.__thread.is_alive():
			logger.debug( 'stop() : thread : join() : start' )
			self.__thread.join()
			logger.debug( 'stop() : thread : join() : finish' )
			pass # END IF

		if hasattr( self.__proc, 'exitstatus' ):
			logger.debug( f'stop() : process : exit status={self.__proc.exitstatus}, signal status={self.__proc.signalstatus}' )
			return ( self.__proc.exitstatus, self.__proc.signalstatus, )

		pass # END METHOD : Stop

	def tailing( self ):
		'''

        Used by your program for determining if a loop should continue checking for output from `rclone`, based upon multiple conditions.

        An example for continuously printing out data from `rclone`:

        .. code-block:: python

            while rclone.tailing():

                if rclone.readline():
                    print( rclone.line, flush=True )

                time.sleep( 0.5 )

        .. seealso::

            :any:`PyClone.readline()`


        Returns
        -------
        :obj:`bool`
            Returns `True` if a process is still running and there's the potential for messages to be added to the buffer, else this returns `False`.

		'''

		# Message queue
		if self.__messages:
			logger.debug( 'tailing() : return : True' )
			return True
			pass # END IF

		# No message queue to process
		elif not isinstance( self.__messages, collections.deque ):
			logger.debug( 'tailing() : return : False' )
			return False
			pass # END IF : No message queue

		# Spawned process has finished
		elif hasattr( self.__proc, 'isalive' ) and not self.__proc.isalive():
			logger.debug( 'tailing() : return : False' )
			return False
			pass # END ELIF : Process finished

		# Process closed and removed
		elif self.__proc is None:
			logger.debug( 'tailing() : return : False' )
			return False

		# Process still running
		else:
			logger.debug( 'tailing() : return : True' )
			return True
			pass # END ELSE

		pass # END METHOD : Tailing

	def readline( self ):
		'''

		Mostly used in conjunction with :any:`PyClone.tailing()`, this retrieves the oldest line from :any:`the message buffer <PyClone.__messages>` that's filled by rclone, with a buffer size set when :any:`initializing the class <PyClone.__init__>`.

		.. seealso::

			:any:`PyClone.tailing()`


		Returns
		-------
		:obj:`bool`
			Returns `True` if a line was removed from the message buffer and stored in :any:`PyClone.line`, otherwise returns `False`.

		'''

		logger.debug( 'readline() : checking for messages' )

		if self.__messages:

			logger.debug( 'readline() : removing element from queue' )
			line	=	self.__messages.popleft()

			if line:
				logger.debug( f'readline() : storing element in self.line : {line}' )
				self.line	=	line
				return True

		return False

		pass # END METHOD : Read line from message buffer

	def clearBuffer( self ):
		'''

		Clear all messages in the buffer that were added by an `rclone` action.

		'''
		logger.debug( 'Clearing message buffer' )
		self.__messages.clear()
		pass # END METHOD : Clear message buffer

	def remotes( self ):
		'''

		Lists configured remotes in `rclone`.


		Returns
		-------
		:obj:`dict`
			Dictionary of available remotes, where the key is the name and the value is the type.

		'''

		logger.debug( 'remotes() : acquire lock' )
		with self.__lock:

			# self.__proc	=	True
			cmdLine		=	f'bash -c "{self.__binPath} {self.__flagsToString()} config dump 2>/dev/null"'
			logger.debug( f'remotes() : spawn process : {cmdLine}' )
			self.__proc	=	pexpect.spawn( cmdLine, echo=False )

			output		=	self.__proc.read( size=-1 ).decode()
			self.__proc.expect( pexpect.EOF )

			logger.debug( 'remotes() : close process' )
			self.__proc.close( force=True )

		logger.debug( 'remotes() : release lock' )

		r	=	{ k:v[ 'type' ] for k,v in json.loads( output ).items() }
		logger.debug( f'remotes() : return : {r}' )
		return r

		pass # END METHOD : List remotes and their reciprocal type.

	def ls( self, remote, path='' ):
		'''

		List files and directories in a given path.  If no path is provided, the root directory of your remote destination will be listed.


		Parameters
		----------
		remote : :obj:`str`
			Name of remote service that's configured in rclone.

		path : :obj:`str`, optional
			Remote path to list.


		Returns
		-------
		list
			Files and directories.

		'''

		logger.debug( f'ls() : remote={remote}, path={path}' )

		logger.debug( 'ls() : acquire lock' )
		with self.__lock:

			cmdLine		=	f'bash -c "{self.__binPath} {self.__flagsToString()} lsjson --max-depth 1 {remote}:{path} 2>/dev/null"'
			logger.debug( f'ls() : spawn process : {cmdLine}' )
			self.__proc	=	pexpect.spawn( cmdLine, echo=False )

			output		=	self.__proc.read( size=-1 ).decode()
			self.__proc.expect( pexpect.EOF )

			logger.debug( 'ls() : close process' )
			self.__proc.close( force=True )

		logger.debug( 'ls() : release lock' )

		r	=	json.loads( output )
		logger.debug( f'ls() : return : {r}' )
		return r

		pass # END METHOD : List files (and directories)

	def __threadedProcess( self, *, action, source, remote, path ):
		'''

		The rclone process runs under this method as a separate thread, which is launched by :any:`PyClone.__launchThread()`.
		All available output from `rclone` is placed into :any:`the message buffer <PyClone.__messages>` from this method.


		Parameters
		----------
		action : :obj:`str`
			Provided by a wrapper method such as :any:`PyClone.copy()` and passed to `rclone`.

		source : :obj:`str`
			Files to transfer.

		remote : :obj:`str`
			Configured service name.

		path : :obj:`str`
			Destination to save to.

		'''

		logger.debug( f'__threadedProcess() : action={action}, source={source}, remote={remote}, path={path}' )

		logger.debug( 'touch() : acquire lock' )
		self.__lock.acquire()

		cmdLine		=	f'bash -c "{self.__binPath} {self.__flagsToString()} --stats=1s --use-json-log --verbose=1 {action} {( source if source else "" )} {remote}:{path} 2>/dev/null"'
		logger.debug( f'__threadedProcess() : spawn process : {cmdLine}' )
		self.__proc	=	pexpect.spawn(
							cmdLine,
							echo	=	False,
							timeout	=	None,
						)

		# Fill buffer
		while not self.__proc.eof():

			line		=	None

			# Parse JSON
			try:
				line	=	json.loads( self.__proc.readline().decode().strip() )
				logger.debug( '__threadedProcess() : parsed JSON line.' )
				pass # END TRY

			# Probably noise from Docker Compose
			except json.JSONDecodeError as e:
				logger.debug( f'__threadedProcess() : exception (JSON decoding error) : {e}' )
				line	=	{}
				pass # END EXCEPTION

			except Exception as e:
				logger.error( f'__threadedProcess() : {e}' )
				pass # END EXCEPTION

			finally:
				logger.debug( f'__threadedProcess() : append message to buffer : {line}' )
				self.__messages.append( line )
				pass # END FINALLY

			pass # END WHILE LOOP

		logger.debug( '__threadedProcess() : close process' )
		self.__proc.close( force=True )

		logger.debug( '__threadedProcess() : release lock' )
		self.__lock.release()

		pass # END PRIVATE METHOD : Threaded process

	def __launchThread( self, *, action, source, remote, path ):
		'''

		This sets up and starts a thread with :any:`PyClone.__threadedProcess()` used as the target,
		and is used by convenience/wrapper methods such as:

		* :any:`PyClone.copy()`

		* :any:`PyClone.sync()`

		* :any:`PyClone.delete()`

		* :any:`PyClone.purge()`


		Parameters
		----------
		action : :obj:`str`
			Provided by a wrapper method such as :any:`PyClone.copy()` and passed to `rclone`.

		source : :obj:`str`
			Files to transfer.

		remote : :obj:`str`
			Configured service name.

		path : :obj:`str`
			Destination to save to.

		'''

		logger.debug( f'__launchThread() : action={action}, source={source}, remote={remote}, path={path}' )
		self.__thread	=	threading.Thread(
							target	=	self.__threadedProcess,
							kwargs	=	{
											'action'	:	action,
											'source'	:	source,
											'remote'	:	remote,
											'path'		:	path,
										}
						)
		logger.debug( f'__launchThread() : start thread' )
		self.__thread.start()

		pass # END PRIVATE METHOD : Launch thread

	def copy( self, *, source, remote, path ):
		'''

		Copy files from source to dest, skipping already copied.


		Parameters
		----------
		source : :obj:`str`
			Files to transfer.

		remote : :obj:`str`
			Configured service name.

		path : :obj:`str`
			Destination to save to.


		.. note::

			This is a convenience method that wraps around :any:`PyClone.__launchThread()`.
			For more information about this action, please read `rclone's documentation <https://rclone.org/commands/rclone_copy/>`_.

		'''

		logger.debug( f'copy() wrapping __launchThread() : source={source}, remote={remote}, path={path}' )
		self.__launchThread( action='copy', source=source, remote=remote, path=path )

		pass # END METHOD : Copy

	def sync( self, *, source, remote, path ):
		'''

		Make source and dest identical, modifying destination only.


		Parameters
		----------
		source : :obj:`str`
			Files to transfer.

		remote : :obj:`str`
			Configured service name.

		path : :obj:`str`
			Destination to save to.


		.. note::

			This is a convenience method that wraps around :any:`PyClone.__launchThread()`.
			For more information about this action, please read `rclone's documentation <https://rclone.org/commands/rclone_sync/>`_.

		'''

		logger.debug( f'sync() wrapping __launchThread() : source={source}, remote={remote}, path={path}' )
		self.__launchThread( action='sync', source=source, remote=remote, path=path )

		pass # END METHOD : Synchronize

	def delete( self, *, remote, path, rmdirs=False ):
		'''

		Remove the contents of path.


		Parameters
		----------
		remote : :obj:`str`
			Configured service name.

		path : :obj:`str`
			Destination to delete.

		rmdirs : :obj:`bool`
			If set to `True`, rclone will remove all empty directories.


		.. seealso::

			:any:`PyClone.purge()` for deleting directories.

		.. note::

			This is a convenience method that wraps around :any:`PyClone.__launchThread()`.
			For more information about this action, please read `rclone's documentation <https://rclone.org/commands/rclone_delete/>`_.

		'''

		logger.debug( f'delete() wrapping __launchThread() : remote={remote}, path={path}, rmdirs={rmdirs}' )
		self.__launchThread( action='delete' + ( ' --rmdirs' if rmdirs else '' ), source=None, remote=remote, path=path )

		pass # END METHOD : Delete

	def purge( self, *, remote, path ):
		'''

		Remove the path and all of its contents.


		Parameters
		----------
		remote : :obj:`str`
			Configured service name.

		path : :obj:`str`
			Destination to delete.


		.. seealso::

			:any:`PyClone.delete()` for deleting files.

		.. note::

			This is a convenience method that wraps around :any:`PyClone.__launchThread()`.
			For more information about this action, please read `rclone's documentation <https://rclone.org/commands/rclone_purge/>`_.

		'''

		logger.debug( f'purge() wrapping __launchThread() : remote={remote}, path={path}' )
		self.__launchThread( action='purge', source=None, remote=remote, path=path )

		pass # END METHOD : Purge

	def touch( self, *, remote, path, create=True, timestamp=None ):
		'''

        Create new file or change file modification time.


        Parameters
        ----------
        remote : :obj:`str`
            Configured service name.

        path : :obj:`str`
            Destination to save to.

        create : :obj:`bool`
            If file doesn't exist, it will be created.

        timestamp : :obj:`str` or :obj:`datetime`
            If timestamp is provided, it will be converted to UTC and applied to the remote service's path.

        Returns
        -------
        bool
            `True` if successful, `False` if unsuccessful.


        .. note::

            For more information about this action, please read `rclone's documentation <https://rclone.org/commands/rclone_touch/>`_.


        Examples:

        .. code-block:: python

            # No timezone provided, will use current UTC.
            rclone.touch( remote='myGoogleDrive', path='/path/to/file.txt' )

            # Date provided, but time (and time zone) has not been.  Time is in UTC.
            rclone.touch( remote='myGoogleDrive', path='/path/to/file.txt', timestamp='2000-01-01' )

            # ISO 8601, in human format with microseconds and without a time zone.  Time is in UTC.
            rclone.touch( remote='myGoogleDrive', path='/path/to/file.txt', timestamp='2000-01-01 12:34:56.789' )

            # ISO 8601, with microseconds and with a time zone.  Time is in Arizona's time zone (they don't waste their time on DST).
            rclone.touch( remote='myGoogleDrive', path='/path/to/file.txt', timestamp='2000-01-01T12:34:56.789-07:00' )

		'''

		logger.debug( f'touch() : remote={remote}, path={path}, create={create}, timestamp={timestamp}' )

		r			=	None

		if timestamp:

			try:
				timestamp	=	arrow.get( timestamp ).to( 'utc' ).format('YYYY-MM-DDTHH:mm:ss.S')

			except arrow.parser.ParserError:
				timestamp	=	None

		try:

			logger.debug( f'touch() : timestamp : {timestamp}' )

			logger.debug( 'touch() : acquire lock' )
			self.__lock.acquire()

			cmdLine		=	f'bash -c "{self.__binPath} {self.__flagsToString()} touch {remote}:{path}{( "" if create else " --no-create " )}{( f" --timestamp {timestamp}" if timestamp else "" )} 2>/dev/null"'
			logger.debug( f'touch() : spawn process : {cmdLine}' )
			self.__proc	=	pexpect.spawn( cmdLine, echo=False )

			output		=	self.__proc.read( size=-1 ).decode()
			self.__proc.expect( pexpect.EOF )

			logger.debug( 'touch() : close process' )
			self.__proc.close( force=True )

			logger.debug( f'touch() : rclone exit status={self.__proc.exitstatus}, signal status={self.__proc.signalstatus}' )
			r			=	True if ( self.__proc.exitstatus == 0 ) else False

		except Exception as e:
			logger.error( e )
			r			=	False

		finally:

			logger.debug( 'touch() : release lock' )
			self.__lock.release()

			logger.debug( f'touch() : return : {r}' )
			return r

		pass # END METHOD : Touch

	pass # END CLASS : PyClone
