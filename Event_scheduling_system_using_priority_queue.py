import heapq
import time
import threading

class Event:
    def __init__(self, name, priority, time_remaining):
        self.name = name
        self.priority = priority
        self.time_remaining = time_remaining

    def __lt__(self, other):
        return self.priority < other.priority

    def __repr__(self):
        return f"Event({self.name}, priority={self.priority}, time_remaining={self.time_remaining})"

class EventScheduler:
    def __init__(self):
        self.event_queue = []
        self.event_list = []
        self.lock = threading.Lock()
        self.halt_event = False
        self.stop_processing = False
        self.is_running = False

    def add_event(self):
        while True:  
            with self.lock:
                event_name = input("Enter event name: ")
                priority = int(input("Enter event priority (lower number = higher priority): "))
                time_remaining = int(input("Enter time remaining (in minutes): "))
                
                new_event = Event(event_name, priority, time_remaining)
                heapq.heappush(self.event_queue, new_event)
                self.event_list.append(new_event)
                print(f"Added event: {event_name} with priority {priority} and time remaining {time_remaining} mins")
    
               
                if self.is_running:
                    self.halt_event = True
                    print("System halted to recheck priorities after adding new event.")

           
            add_more = input("Do you want to add another event? (yes/no): ").strip().lower()
            if add_more != 'yes':
                break

    def remove_event(self, event_name):
        with self.lock:
            self.event_list = [event for event in self.event_list if event.name != event_name]
            self.event_queue = [event for event in self.event_queue if event.name != event_name]
            heapq.heapify(self.event_queue)
            print(f"Removed event: {event_name}")

    def update_priorities(self):
        with self.lock:
            for event in self.event_list:
                event.priority = max(1, 10 - event.time_remaining // 10)
            heapq.heapify(self.event_queue)

    def decrease_time(self, minutes):
        with self.lock:
            for event in self.event_list:
                event.time_remaining = max(0, event.time_remaining - minutes)

    def process_next_event(self):
        with self.lock:
            if self.event_queue and not self.halt_event:
                next_event = heapq.heappop(self.event_queue)
                print(f"Processing event: {next_event.name} with priority {next_event.priority} (time remaining: {next_event.time_remaining} mins)")
                self.event_list.remove(next_event)
                return next_event
            else:
                return None

    def display_events(self):
        with self.lock:
            if self.event_list:
                print("\nCurrent events in the system:")
                for event in self.event_list:
                    print(f"Event: {event.name}, Priority: {event.priority}, Time remaining: {event.time_remaining} mins")
            else:
                print("No events in the system.")

    def display_next_event(self):
        with self.lock:
            if self.event_queue:
                next_event = self.event_queue[0]
                print(f"Next event to process: {next_event.name} (Priority: {next_event.priority}, Time remaining: {next_event.time_remaining} mins)")
            else:
                print("No more events to process.")

    def halt_current_event(self):
        with self.lock:
            self.halt_event = True
            print("Halted current event processing.")

    def stop_scheduler(self):
        with self.lock:
            self.stop_processing = True
            self.is_running = False
            print("Stopping event scheduler...")

    def event_processing_with_timer(self, interval_seconds):
        while not self.stop_processing:
            if self.is_running:
                self.decrease_time(interval_seconds // 60)
                self.update_priorities()
                self.display_events()
                next_event = self.process_next_event()

                if next_event is not None:
                    for _ in range(interval_seconds):
                        time.sleep(1)
                        if self.halt_event:
                            print(f"Event {next_event.name} processing halted.")
                            self.remove_event(next_event.name)
                            self.halt_event = False
                            break

                    if not self.halt_event:
                        print(f"Completed event: {next_event.name}")
                else:
                    print("No more events to process.")
                    self.is_running = False
            else:
                time.sleep(1)

        print("Event scheduler stopped.")

    def start_system(self):
        with self.lock:
            if not self.is_running:
                self.is_running = True
                print("System started. Events are being processed.")
            else:
                print("System is already running.")


def user_interaction(scheduler):
    while not scheduler.stop_processing:
        print("\nOptions:")
        print("1. Add an event")
        print("2. Remove an event")
        print("3. Halt current event")
        print("4. Stop the scheduler")
        print("5. Display current events")
        print("6. Start the system")
        print("7. Display next event to process")
        option = input("Choose an option (1-7): ")

        if option == '1':
            scheduler.add_event() 
        elif option == '2':
            event_name = input("Enter the name of the event to remove: ")
            scheduler.remove_event(event_name)
        elif option == '3':
            scheduler.halt_current_event()
        elif option == '4':
            scheduler.stop_scheduler()
        elif option == '5':
            scheduler.display_events()
        elif option == '6':
            scheduler.start_system()
        elif option == '7':
            scheduler.display_next_event()
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    scheduler = EventScheduler()
 
    scheduler_thread = threading.Thread(target=scheduler.event_processing_with_timer, args=(10,))
    scheduler_thread.start()
 
    user_interaction(scheduler)

    scheduler_thread.join()
