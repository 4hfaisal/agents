# Event Status Guide

## Status Values

**interested**
- Event is on the radar
- Waiting for official dates or more information
- No commitment yet

**planning**
- Dates confirmed and user wants to attend
- Actively working on logistics (registration, travel, accommodation)
- May need reminders for deadlines

**committed**
- Fully registered/accommodation booked
- Travel arrangements confirmed
- Ready to attend

**declined**
- User decided not to attend this occurrence
- May reconsider in future years
- Decision log explains reasoning

**attended**
- Successfully attended the event
- Historical record for reference

**cancelled**
- Event was cancelled or postponed by organizers
- No action needed from user

## Status Transitions

```
interested → planning → committed → attended
interested → declined
interested → cancelled
planning → declined
planning → cancelled
```
