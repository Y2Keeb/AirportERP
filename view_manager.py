class ViewManager:
    def __init__(self, root):
        self.root = root
        self.current_view = None
        self.view_stack = []
        self.shared_state = {}  # For storing user_id, username, etc.

    def show_view(self, view_class, *args, **kwargs):
        """Show a new view with proper state management"""
        # Clean up current view if exists
        if hasattr(self, 'current_view') and self.current_view:
            self.current_view.cleanup()

        # Create new view
        self.current_view = view_class(self.root, *args, **kwargs)

        # Add to view stack
        self.view_stack.append((view_class, kwargs))
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

    def pop_view(self, **kwargs):
        """Pop the current view from the stack"""
        if len(self.view_stack) > 1:
            self.view_stack[-1].cleanup()
            self.view_stack.pop()
            prev_view_class, prev_state = self.view_stack[-1]
            prev_state.update(kwargs)
            self.current_view = prev_view_class(self.root, **prev_state)
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