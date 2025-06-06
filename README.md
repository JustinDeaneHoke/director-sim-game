# director-sim-game
A web-based text simulation game where players build a career as a film, TV, or commercial director.

## Development

Pages and components are located in `src/`. The `Production` page displays live updates from the production process. It uses Tailwind CSS classes for styling.

### Production Page
- **src/pages/Production.jsx**: Fetches production data via POST `/start_production`, shows logs using `ProductionLog` and lets the player finish production which posts to `/release_project`.
- **src/components/ProductionLog.jsx**: Renders production notes as a timeline-styled list.
