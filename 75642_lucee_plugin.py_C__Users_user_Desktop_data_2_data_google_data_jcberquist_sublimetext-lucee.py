import sublime, sublime_plugin, webbrowser
from .src.bootstrap import *
from .src import completions, events, utils

class LuceeEventListener(sublime_plugin.EventListener):
	"""
	Event Listener for Lucee/CFML
	"""
	def on_load_async(self, view):
		events.trigger('on_load_async', view)

	def on_close(self, view):
		events.trigger('on_close', view)

	def on_post_save_async(self, view):
		events.trigger('on_post_save_async', view)

	def on_post_text_command(self, view, command_name, args):
		if command_name == "commit_completion":
			pos = view.sel()[0].begin()
			if view.match_selector(pos, "embedding.cfml meta.tag.cfml - source.cfml.script, embedding.cfml meta.tag.script.cfml"):
				view.run_command("auto_complete", {"api_completions_only": True})

	def on_query_completions(self, view, prefix, locations):
		for dialect in ["lucee","cfml"]:
			if not view.match_selector(locations[0], "embedding." + dialect):
				continue

			prefix_start = locations[0] - len(prefix)
			base_script_scope = "embedding." + dialect + " source." + dialect + ".script"

			# tag completions
			if view.match_selector(prefix_start, "embedding." + dialect + " - source." + dialect + ".script"):
				tag_completions = completions.get_tag_completions(view, prefix, locations[0], dialect)
				return tag_completions

			# dot completions (member and model function completions)
			if view.match_selector(prefix_start - 1, base_script_scope + " keyword.operator.accessor." + dialect):
				completion_list = completions.get_dot_completions(view, prefix, locations[0], dialect)
				return completion_list

			#tag in script attribute completions
			if view.match_selector(prefix_start, base_script_scope + " meta.tag, " + base_script_scope + " meta.class"):
				attribute_completions = completions.get_script_tag_attributes(view, prefix, locations[0], dialect)
				return attribute_completions

			# script completions
			if view.match_selector(prefix_start, "embedding." + dialect + " source." + dialect + ".script"):
				completion_list = completions.get_script_completions(view, prefix, locations[0], dialect)
				return completion_list

		# default
		return None

class LuceeDocsCommand(sublime_plugin.TextCommand):

	def run(self, edit):
		pt = self.view.sel()[0].begin()
		word_tuple = None

		if self.view.match_selector(pt, "support.function.lucee"):
			word_tuple = self.view.substr(self.view.word(pt)).lower(), "functions"
		elif self.view.match_selector(pt, "meta.tag.lucee"):
			word_tuple = utils.get_tag_name(self.view, pt)[1:], "tags"
		elif self.view.match_selector(pt, "meta.tag.script.lucee"):
			word_tuple = utils.get_tag_name(self.view, pt), "tags"

		if word_tuple:
			full_url = "http://docs.lucee.org/reference/" + word_tuple[1] + "/" + word_tuple[0] + ".html"
			webbrowser.open_new_tab(full_url)

class CloseLuceeTagCommand(sublime_plugin.TextCommand):

	def run(self, edit):
		pt = self.view.sel()[0].begin()
		lucee_only = self.view.match_selector(pt, "string")
		last_open_tag = utils.get_last_open_tag(self.view,pt - 1, lucee_only)
		if last_open_tag:
			self.view.insert(edit,pt,"/" + last_open_tag + ">")
		else:
			# if there is no open tag print "/"
			self.view.insert(edit,pt,"/")

class LuceeDefaultPackageSettingsCommand(sublime_plugin.WindowCommand):

	def run(self):
		self.window.run_command("open_file", {"file": "${packages}/" + utils.get_plugin_name() + "/settings/lucee_package.sublime-settings"})
