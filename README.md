# HSL Planner

This program makes use of the [Digitransit](https://digitransit.fi/en/developers/) GraphQL APIs to gather realtime route data from the Helsinki [HSL Transit Network](https://www.hsl.fi/en).

I've built this project to gather realtime departure information from my local transit stops (accounting for delays, cancellations, route changes, etc...) to display the results in my home.

---

### Using the Program

1. Fork the repository and clone it to your local machine

2. Add a `.env` file to the root folder of your project, with the following information

   - `API_KEY` is provided after signing up for a development account on the [Digitransit Portal](https://portal-api.digitransit.fi/)
   - `STOP_IDS` should be set to your preferred HSL stop location(s). See [Digitransit Documentation](https://digitransit.fi/en/developers/apis/1-routing-api/stops/) for details.
     - Supports a single stop (ex. "HSL:11235") or multiple stops in csv format (ex. "HSL:11235,HSL:81321")

   ```
   API_ENDPOINT="https://api.digitransit.fi/routing/v2/hsl/gtfs/v1"

   API_KEY=[YOUR-API-KEY]

   STOP_IDS=[YOUR-STOP-IDS]
   ```

3. Run the `main.py` file from the command line

---

### Future Features

- [x] Connect to Digitransit API to retrieve local departure information
- [x] Track multiple STOP_ID values at the same time
- [ ] Filter to only show preferred routes from each tracked STOP_ID.
- [ ] Interface with a display technology (ex. [TRMNL](https://usetrmnl.com/)) running a service to update the results at regular intervals
