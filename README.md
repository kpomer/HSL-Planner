# HSL Planner

This program makes use of the [Digitransit](https://digitransit.fi/en/developers/) GraphQL APIs to gather realtime route data from the Helsinki [HSL Transit Network](https://www.hsl.fi/en) using GraphQL.

I've built this project to gather the realtime departure schedule from my local transit stops (taking into account delays and cancellations), and display these details in my house.

---

### Using the Program

1. Fork the repository and clone it to your local machine

2. Add a `.env` file to the root folder of your project, with the following information
   - `API_KEY` is provided after signing up for a development account on the [Digitransit Portal](https://portal-api.digitransit.fi/)
   - `STOP_ID` should be set for your preferred HSL stop location. See [Digitransit Documentation](https://digitransit.fi/en/developers/apis/1-routing-api/stops/) for details

```
API_ENDPOINT="https://api.digitransit.fi/routing/v2/hsl/gtfs/v1"

API_KEY=[YOUR-API-KEY]

STOP_ID=[YOUR-STOP-ID]
```

---

### Future Features

- [ ] Track multiple STOP_IDs at the same time
- [ ] Allow data to be shown on a display (ex. [TRMNL](https://usetrmnl.com/)) which updates at regular intervals
