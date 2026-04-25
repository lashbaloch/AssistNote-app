# AGENTS.md

## Project goal
Build a polished mobile-first GUI prototype for AssistNote, a university project for Australian banknote detection using a trained YOLO model.

## Main priorities
1. Keep the app simple, clean, and demo-friendly.
2. Make the UI feel like a mobile assistive app.
3. Support image upload first.
4. Structure the code so live camera can be added easily later.
5. Use the provided YOLO model at app/models/best.pt.
6. Use the class labels from app/config/classes.json.
7. Add text-to-speech audio feedback.
8. Keep code modular:
   - UI
   - inference
   - utilities
9. Add clear run instructions and requirements.
10. Prefer practical implementation over overengineering.

## UI style
- high contrast
- large buttons
- minimal clutter
- modern card layout
- accessible spacing
- polished typography
- suitable for university demo

## Functional behavior
- show detected image with boxes
- show denominations and confidence
- count detected notes
- if confidence is low, say and show retry guidance
