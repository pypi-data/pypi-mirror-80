#!/usr/bin/env python -u
# -*- coding: utf-8 -*-

# System
import sys
import os

# PyPI
import setuptools

# Used for updating copyright data in Sphinx.
from datetime import date

# Module information
name			=	"PyClone"
__version__		=	( '2020', '09', 'a1' )	# See https://packaging.python.org/guides/distributing-packages-using-setuptools/#standards-compliance-for-interoperability
version			=	f'{ __version__[ 0 ] }.{ __version__[ 1 ] }'
release			=	f'{ __version__[ 0 ] }.{ __version__[ 1 ] }{ __version__[ 2 ] }'
author			=	"Louis T. Getterman IV"
author_email	=	"Thad@Getterman.org"
description		=	"Wraps rclone and provides an interface for an installation at the host or container level."
license			=	"MIT"
project_urls	=	{
						'Documentation'	:	'https://ltgiv.gitlab.io/pyclone/',
						'Source'		:	'https://gitlab.com/ltgiv/pyclone',
						'Tracker'		:	'https://gitlab.com/ltgiv/pyclone/issues',
					}

pathBase		=	os.path.abspath( os.path.dirname( sys.argv[ 0 ] ) )

# Generating documentation
# python setup.py build_sphinx
if ( len( sys.argv ) > 1 ) and sys.argv[ 1 ] == 'build_sphinx':
	from sphinx.setup_command import BuildDoc
	pass # END IF

# Probably deploying to PyPI, and Sphinx isn't needed.
# twine upload --skip-existing --repository-url https://test.pypi.org/legacy/ dist/*
else:
	BuildDoc	=	None
	pass # END ELSE

if __name__ == '__main__':

	with open( os.path.join( pathBase, "README.md" ), "r" ) as fh:
		long_description	=	fh.read()

	setuptools.setup(
		name							=	name,
		version							=	release,
		author							=	author,
		author_email					=	author_email,
		description						=	description,
		# requires = [ line.strip('\n') for line in open( 'requirements.txt' ).readlines() ],		# Frowned upon way of adding in dependencies - see https://caremad.io/posts/2013/07/setup-vs-requirement/
		install_requires				=	[
												'Logbook',
												# 'psutil',
												# 'munch',
												'pexpect',
											],
		long_description				=	long_description,
		long_description_content_type	=	"text/markdown",
		license							=	license,
		url								=	project_urls[ 'Source' ],
		project_urls					=	project_urls,
# FIX: check into find_namespace_package() for modules without __init__.py
		packages						=	setuptools.find_packages(),
		classifiers						=	[
												"Programming Language :: Python :: 3",
												"License :: OSI Approved :: MIT License",
												"Operating System :: POSIX",
												"Development Status :: 3 - Alpha",
											],
		cmdclass						=	{
												'build_sphinx'	:	BuildDoc,
											},
		command_options					=	{
												'build_sphinx'	:	{
																		'project'		:	( 'setup.py', name, ),
																		'copyright'		:	( 'setup.py', f'{ int( date.today().year ) }, { author }' ),
																		# 'author'		:	( 'setup.py', author, ),
																		'version'		:	( 'setup.py', version, ),
																		'release'		:	( 'setup.py', release, ),
																		'source_dir'	:	( 'setup.py', os.path.join( pathBase, 'docs', 'source', ) ),
																		'build_dir'		:	( 'setup.py', os.path.join( pathBase, 'docs', 'build', ) ),
																	}
											},
	)

	pass # END MAIN
