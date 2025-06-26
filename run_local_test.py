import logging
from STRCalendarEmailSend import main

# Mock TimerRequest for local testing.
class MockTimerRequest:
    """Mock TimerRequest for local testing."""
    def __init__(self, past_due=False):
        self.past_due = past_due

if __name__ == '__main__':
    # Set up basic logging
    logging.basicConfig(level=logging.INFO)

    # Mock a timer request for local testing
    mock_timer = MockTimerRequest()
    
    print("--- Running local test ---")
    main(mock_timer)
    print("--- Local test finished ---")
