# Event-scheduling-system-using-priority-queue.-
This Python-based Event Scheduler System is a multithreaded application that prioritizes and processes events using a priority queue. It allows users to manage events dynamically, making it a powerful tool for scheduling and organizing tasks.
Features
Add Events
Add multiple events with custom names, priorities, and time remaining. Events with lower priority values (higher importance) are processed first.

Remove Events
Remove specific events by their name to dynamically update the schedule.

Dynamic Priority Management
Ensures events are processed based on their priority, with users having full control over scheduling.

Event Processing
Automatically processes events in priority order, decrementing time and updating the schedule in real-time.

Halt and Resume
Halt the current event's processing and make adjustments without losing progress.

Display Options

View a list of all events with details like name, priority, and remaining time.
See the next event in the queue that is ready for processing.
Interactive Menu
A user-friendly menu-driven interface for easy interaction with the system.

Multithreading
Event processing operates on a separate thread, enabling simultaneous user interaction and task handling.

Stop Scheduler
Gracefully stop the system when all events are processed or upon user request.
