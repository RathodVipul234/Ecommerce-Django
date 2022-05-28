from django.views import View
from django.shortcuts import render, redirect


class LoginRequiredMixin(View):
	"""Login required mixin"""
	def dispatch(self, request, *args, **kwargs):
		if self.request.user.is_authenticated:
			return super().dispatch(request, *args, **kwargs)
		return redirect("login")

		