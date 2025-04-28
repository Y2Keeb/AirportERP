class ViewManager:
    def __init__(self, root):
        self.root = root
        self.current_view = None
        self.view_stack = []
        self.shared_state = {}  # For storing user_id, username, etc.

    def show_view(self, view_class, *args, **kwargs):
        """Completely replace current view"""
        self._cleanup_current_view()
        kwargs['view_manager'] = self
        self.current_view = view_class(self.root, *args, **kwargs)
        return self.current_view

    def push_view(self, view_class, *args, **kwargs):
        """Completely replace current view with new one"""
        if self.current_view:
            if hasattr(self.current_view, 'cleanup'):
                self.current_view.cleanup()
            elif hasattr(self.current_view, 'destroy'):
                self.current_view.destroy()

        if hasattr(self.current_view, 'view_state'):
            self.view_stack.append((self.current_view.__class__, self.current_view.view_state))

        final_kwargs = kwargs.copy()
        final_kwargs['view_manager'] = self
        final_kwargs['root'] = self.root

        self.current_view = view_class(**final_kwargs)
        return self.current_view

    def pop_view(self):
        if self.current_view:
            if hasattr(self.current_view, 'cleanup'):
                self.current_view.cleanup()
            elif hasattr(self.current_view, 'destroy'):
                self.current_view.destroy()

        if self.view_stack:
            view_class, state = self.view_stack.pop()
            self.current_view = view_class(self.root, **state)
            return self.current_view
        return None

    def _cleanup_current_view(self):
        """Clean up current view resources"""
        if self.current_view:
            if hasattr(self.current_view, 'cleanup'):
                self.current_view.cleanup()
            elif hasattr(self.current_view, 'destroy'):
                self.current_view.destroy()
            elif hasattr(self.current_view, 'frame_main'):
                self.current_view.frame_main.destroy()

    def reset(self):
        """Reset entire navigation"""
        self._cleanup_current_view()
        self.current_view = None
        self.view_stack = []
        self.shared_state = {}