"""
Progress Tracking System for Global Underwriting Jira Integration
Provides real-time progress updates for long-running operations
"""
import json
import time
import uuid
from typing import Dict, Optional, Callable
from threading import Thread, Event
import logging

logger = logging.getLogger(__name__)

class ProgressTracker:
    """Manages progress tracking for long-running operations"""
    
    def __init__(self):
        self.active_operations = {}  # operation_id -> OperationProgress
        self.event_listeners = {}    # operation_id -> list of event queues
        
    def start_operation(self, operation_type: str, total_steps: int = 100, 
                       operation_name: str = None) -> str:
        """Start tracking a new operation"""
        operation_id = str(uuid.uuid4())
        operation_name = operation_name or f"{operation_type} Operation"
        
        progress = OperationProgress(
            operation_id=operation_id,
            operation_type=operation_type,
            operation_name=operation_name,
            total_steps=total_steps
        )
        
        self.active_operations[operation_id] = progress
        self.event_listeners[operation_id] = []
        
        logger.info(f"Started operation {operation_id}: {operation_name}")
        return operation_id
        
    def update_progress(self, operation_id: str, current_step: Optional[int], 
                       status_message: str = None, details: Dict = None):
        """Update progress for an operation"""
        if operation_id not in self.active_operations:
            logger.warning(f"Operation {operation_id} not found")
            return
            
        progress = self.active_operations[operation_id]
        progress.update(current_step, status_message, details)
        
        # Notify all listeners
        self._notify_listeners(operation_id, progress.to_dict())
        
    def complete_operation(self, operation_id: str, success: bool = True, 
                          final_message: str = None, results: Dict = None):
        """Mark an operation as completed"""
        if operation_id not in self.active_operations:
            logger.warning(f"Operation {operation_id} not found")
            return
            
        progress = self.active_operations[operation_id]
        progress.complete(success, final_message, results)
        
        # Final notification
        self._notify_listeners(operation_id, progress.to_dict())
        
        logger.info(f"Completed operation {operation_id}: {'Success' if success else 'Failed'}")
        
        # Clean up after a delay to allow final event delivery
        def cleanup():
            time.sleep(2)
            self.active_operations.pop(operation_id, None)
            self.event_listeners.pop(operation_id, None)
            
        Thread(target=cleanup, daemon=True).start()
        
    def add_listener(self, operation_id: str, event_queue):
        """Add an event listener for an operation"""
        if operation_id in self.event_listeners:
            self.event_listeners[operation_id].append(event_queue)
            
    def remove_listener(self, operation_id: str, event_queue):
        """Remove an event listener"""
        if operation_id in self.event_listeners:
            try:
                self.event_listeners[operation_id].remove(event_queue)
            except ValueError:
                pass
                
    def get_operation_progress(self, operation_id: str) -> Optional[Dict]:
        """Get current progress for an operation"""
        progress = self.active_operations.get(operation_id)
        return progress.to_dict() if progress else None
        
    def _notify_listeners(self, operation_id: str, progress_data: Dict):
        """Notify all listeners of progress update"""
        if operation_id not in self.event_listeners:
            return
            
        dead_listeners = []
        for event_queue in self.event_listeners[operation_id]:
            try:
                event_queue.put(progress_data)
            except Exception as e:
                logger.warning(f"Failed to notify listener: {e}")
                dead_listeners.append(event_queue)
                
        # Clean up dead listeners
        for dead_listener in dead_listeners:
            self.event_listeners[operation_id].remove(dead_listener)

class OperationProgress:
    """Represents progress of a single operation"""
    
    def __init__(self, operation_id: str, operation_type: str, 
                 operation_name: str, total_steps: int):
        self.operation_id = operation_id
        self.operation_type = operation_type
        self.operation_name = operation_name
        self.total_steps = total_steps
        self.current_step = 0
        self.status = "running"
        self.status_message = "Starting..."
        self.start_time = time.time()
        self.end_time = None
        self.details = {}
        self.results = {}
        
    def update(self, current_step: Optional[int], status_message: str = None, 
               details: Dict = None):
        """Update progress information"""
        # Only update current_step if a valid step is provided
        if current_step is not None:
            self.current_step = min(current_step, self.total_steps)
        if status_message:
            self.status_message = status_message
        if details:
            self.details.update(details)
            
    def complete(self, success: bool = True, final_message: str = None, 
                results: Dict = None):
        """Mark operation as completed"""
        self.current_step = self.total_steps
        self.status = "completed" if success else "failed"
        self.end_time = time.time()
        
        if final_message:
            self.status_message = final_message
        elif success:
            self.status_message = "Operation completed successfully"
        else:
            self.status_message = "Operation failed"
            
        if results:
            self.results = results
            
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization"""
        duration = (self.end_time or time.time()) - self.start_time
        percentage = (self.current_step / self.total_steps * 100) if self.total_steps > 0 else 0
        
        return {
            "operation_id": self.operation_id,
            "operation_type": self.operation_type,
            "operation_name": self.operation_name,
            "total_steps": self.total_steps,
            "current_step": self.current_step,
            "percentage": round(percentage, 1),
            "status": self.status,
            "status_message": self.status_message,
            "duration": round(duration, 1),
            "details": self.details,
            "results": self.results if self.status in ["completed", "failed"] else {}
        }

# Global progress tracker instance
progress_tracker = ProgressTracker()

def run_with_progress(operation_type: str, operation_name: str, 
                     operation_func: Callable, *args, **kwargs):
    """
    Decorator to run a function with progress tracking
    The function should accept 'progress_callback' as a keyword argument
    """
    operation_id = progress_tracker.start_operation(operation_type, operation_name=operation_name)
    
    def progress_callback(step: Optional[int], message: str = None, details: Dict = None, total: int = None):
        if total:
            progress_tracker.active_operations[operation_id].total_steps = total
        progress_tracker.update_progress(operation_id, step, message, details)
    
    try:
        # Add progress callback to function arguments
        kwargs['progress_callback'] = progress_callback
        kwargs['operation_id'] = operation_id
        
        result = operation_func(*args, **kwargs)
        progress_tracker.complete_operation(operation_id, True, results={"data": result})
        return result, operation_id
        
    except Exception as e:
        logger.exception(f"Operation {operation_id} failed")
        progress_tracker.complete_operation(
            operation_id, 
            False, 
            f"Operation failed: {str(e)}"
        )
        raise e