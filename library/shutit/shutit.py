#Copyright (C) 2014 OpenBet Limited
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is furnished
#to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
#FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
#COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
#IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
#CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from shutit_module import ShutItModule
import util

class shutit(ShutItModule):

	# check_ready
	# 
	# Check whether we are ready to build this module.
	# 
	# This is called before the build, to ensure modules have 
	# their requirements in place (eg files required to be mounted 
	# in /resources). Checking whether the build will happen (and
	# therefore whether the check should take place) will be 
	# determined by the framework.
	# 
	# Should return True if it ready, else False.
	def check_ready(self,shutit):
		return True

	# is_installed
	#
	# Determines whether the module has been built in this container
	# already.
	#
	# Should return True if it is certain it's there, else False.
	def is_installed(self,shutit):
		container_child = util.get_pexpect_child('container_child')
		root_prompt_expect = shutit.cfg['expect_prompts']['root_prompt']
		return util.file_exists(container_child,'/shutit',root_prompt_expect)

	# build
	#
	# Run the build part of the module, which should ensure the module
	# has been set up.
	# If is_installed determines that the module is already there,
	# this is not run.
	#
	# Should return True if it has succeeded in building, else False.
	def build(self,shutit):
		container_child = util.get_pexpect_child('container_child') # Let's get the container child object from pexpect.
		root_prompt_expect = shutit.cfg['expect_prompts']['root_prompt'] # Set the string we expect to see once commands are done.
		util.install(container_child,shutit.cfg,'git',root_prompt_expect)
		util.send_and_expect(container_child,'pushd /',root_prompt_expect)
		util.send_and_expect(container_child,'git clone https://github.com/ianmiell/shutit.git',root_prompt_expect)
		util.send_and_expect(container_child,'popd /',root_prompt_expect)
		# TODO need to add user
		return True

	# start
	#
	# Run when module should be installed (is_installed() or configured to build is true)
	# Run after repo work.
	def start(self,shutit):
		return True

	# stop
	#
	# Run when module should be stopped.
	# Run before repo work, and before finalize is called.
	def stop(self,shutit):
		return True

	# cleanup
	#
	# Cleanup the module, ie clear up stuff not needed for the rest of the build, eg tar files removed, apt-get cleans.
	# Should return True if all is OK, else False.
	# Note that this is only run if the build phase was actually run.
	def cleanup(self,shutit):
		return True

	# finalize
	#
	# Finalize the module, ie do things that need doing before we exit.
	def finalize(self,shutit):
		return True

	# remove
	# 
	# Remove the module, which should ensure the module has been deleted 
	# from the system.
	def remove(self,shutit):
		return True

	# test
	#
	# Test the module is OK.
	# Should return True if all is OK, else False.
	# This is run regardless of whether the module is installed or not.
	def test(self,shutit):
		return True

	# get_config
	#
	# each object can handle config here
	def get_config(self,shutit):
		cp = shutit.cfg['config_parser']
		return True


if not util.module_exists('shutit.tk.shutit.shutit'):
	obj = shutit('shutit.tk.shutit.shutit',0.397)
	obj.add_dependency('shutit.tk.setup')
	obj.add_dependency('shutit.tk.docker.docker')
	# We need to create a user to get shutit to work
	obj.add_dependency('shutit.tk.adduser.adduser')
	util.get_shutit_modules().add(obj)
	ShutItModule.register(shutit)

