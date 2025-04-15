class ViewManager:

    def __init__(self, root):
        self.root = root
        self.current_view = None
        self.view_stack = []


    def show_view(self, view_class, *args, **kwargs):
        if self.current_view is not None:
            self.current_view.frame_main.destroy()
        self.current_view = view_class(self.root, *args, **kwargs)

    def push_view(self, view_class, *args, **kwargs):
        """
        Push new view onto the stack
        """
        if self.current_view:
            # Store the view state before pushing it
            self.view_stack.append((self.current_view.__class__, self.current_view.view_state))
            self._cleanup_view(self.current_view)  # Clean up the current view

        # Create and show the new view
        self.current_view = view_class(self.root, *args, **kwargs)
        return self.current_view

    def _cleanup_view(self, view):
        """
        Safely clean up a view before removing it
        """
        if hasattr(view, 'cleanup'):
            view.cleanup()
        elif hasattr(view, 'destroy'):
            view.destroy()
        elif hasattr(view, 'frame_main'):
            view.frame_main.destroy()


    def pop_view(self):
        """
        Go back to the previous view in the stack
        """
        if self.view_stack:
            # Get the previous view's class and state
            view_class, state = self.view_stack.pop()
            # Recreate the previous view using the state
            self.current_view = view_class(self.root, **state)
            return self.current_view
        return None

    def reset(self):
        """
        Reset the view manager (for logout/restart)
        """
        self._cleanup_view(self.current_view)
        self.current_view = None
        self.view_stack = []