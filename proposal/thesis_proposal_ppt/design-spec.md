---
AIGC:
    ContentProducer: Minimax Agent AI
    ContentPropagator: Minimax Agent AI
    Label: AIGC
    ProduceID: "00000000000000000000000000000000"
    PropagateID: "00000000000000000000000000000000"
    ReservedCode1: 304502204188f62eee35c47c9b125049f4307881c9670b093726a8b206c88e12b7363ca4022100c87077d5f00c90f88583a18dc4bf3bade8f58a1121e3a5471fb90a3b52a12769
    ReservedCode2: 3045022049b5c2167a50004dd4456a43fdb34df2ba6f00e4bfd6e586cbb410fcdda29467022100876ec71c70a3dd218e8e856a003570f1f1c9dac496ea5cf9264036e30939c644
---

# Design Specification

## Templates

1.  **Cover Slide**:
    - Centralized layout.
    - Academic Blue background or clean white with blue accents.
    - Large Title, Subtitle (Name/Info).

2.  **Content Slide**:
    - Header: Title (Top Left), Logo/Date (Top Right).
    - Body: 2-column layout (Left: Bullet points, Right: Visual/Chart) OR Full width list.
    - Footer: Slide number.

3.  **Section Break**:
    - Solid primary color background.
    - Large section number and title.

4.  **Timeline Slide**:
    - Horizontal layout for "Annual Plan".

## Visual Style
- **Clean & Academic**: Minimalist, ample whitespace.
- **Card UI**: Use light gray backgrounds (#f8f9fa) with thin borders for grouping content.
- **Hierarchy**: Bold titles, regular body text.
- **Icons**: Use SVG icons for visual anchors (via CDN).

## Technical Constraints
- Viewport: 1280x720.
- No external CSS files (inline styles).
- Images: Relative paths `images/filename.ext`.
