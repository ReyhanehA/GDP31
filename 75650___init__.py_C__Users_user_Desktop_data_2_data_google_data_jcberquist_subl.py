import sublime_plugin
from .controller_view_toggle import toggle_controller_view

class LuceeToggleControllerViewCommand(sublime_plugin.TextCommand):

	def run(self, edit):
		toggle_controller_view(self.view, self.view.sel()[0].begin())