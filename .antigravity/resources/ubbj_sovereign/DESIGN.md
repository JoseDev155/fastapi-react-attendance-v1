# Design System Document: The Sovereign Ledger

## 1. Overview & Creative North Star
**Creative North Star: "The Academic Vault"**
This design system rejects the "SaaS-standard" look of bright outlines and flat grids. Instead, it draws inspiration from high-end private banking and archival scholarship. It treats educational data not as a series of rows, but as a prestigious ledger. 

The aesthetic is defined by **Tonal Architecture**: hierarchy is established through overlapping layers of light and shadow rather than structural lines. By utilizing intentional asymmetry—such as wide margins on one side and compact data on the other—we break the "template" feel, creating a digital experience that feels bespoke, authoritative, and permanent.

---

## 2. Color Theory & Tonal Depth
The palette utilizes a sophisticated "Institutional Red" (`#ffb4ac` to `#a82020`) against a base of "Obsidian" (`#121314`). 

### The "No-Line" Rule
**Borders are a failure of hierarchy.** In this system, 1px solid borders are strictly prohibited for sectioning. Boundaries must be defined solely through:
1.  **Background Shifts:** Transitioning from `surface` to `surface-container-low`.
2.  **Negative Space:** Using the Spacing Scale (specifically `spacing.8` and `spacing.12`) to isolate modules.
3.  **Tonal Transitions:** A subtle shift from `surface-container-lowest` to `surface-container-high` to imply a clickable area.

### Surface Hierarchy & Nesting
Treat the UI as physical layers of frosted glass.
*   **Base Layer:** `surface` (#121314).
*   **Secondary Sectioning:** `surface-container-low` (#1b1c1d).
*   **Actionable Cards:** `surface-container-highest` (#343536).
*   **Active Overlays:** `surface-bright` (#38393a).

### The Glass & Gradient Rule
To provide "visual soul," primary CTAs must use a linear gradient from `primary` (#ffb4ac) to `primary_container` (#a82020) at a 135-degree angle. Floating elements (modals/drawers) should use `surface_container_highest` with a 12px `backdrop-blur` and 40% opacity to allow the institutional red accents to bleed through from the layers below.

---

### 3. Typography: The Editorial Scale
We pair the geometric authority of **Instrument Sans** (Headings) with the utilitarian precision of **Inter** (Data).

*   **The Power Hierarchy:**
    *   **Display/Headline (Instrument Sans):** Used for student names, total attendance percentages, and page titles. High tracking (-0.02em) for a premium feel.
    *   **Title/Body (Inter):** Used for administrative data, table headers, and form labels.
*   **Intentional Contrast:** Always pair a `headline-lg` in `on_surface` with a `label-md` in `on_surface_variant` (Ochre/Red tint) to create an immediate focal point.

---

## 4. Elevation & Depth
### The Layering Principle
Never use a shadow where a color shift will suffice. Place a `surface-container-lowest` (#0d0e0f) card inside a `surface-container-low` (#1b1c1d) section to create a "recessed" look, perfect for data entry fields.

### Ambient Shadows
For floating elements like dropdowns, use "The Sovereign Shadow":
*   **Color:** `rgba(13, 14, 15, 0.6)` (a tint of the background, never pure black).
*   **Blur:** 40px to 60px.
*   **Spread:** -5px.
This creates a natural "lift" rather than a harsh cutout.

### The "Ghost Border" Fallback
If a border is required for accessibility (e.g., in high-contrast mode), use a "Ghost Border": `outline_variant` at **15% opacity**. 

---

## 5. Component Guidelines

### Buttons: The Signature Action
*   **Primary:** Gradient fill (`primary` to `primary_container`), `rounded-md` (0.375rem). No border.
*   **Secondary:** Ghost style. Transparent background, `ghost-border` (15% opacity), text in `primary`.
*   **States:** On hover, the `surface_tint` should create a subtle inner glow (box-shadow: inset 0 0 10px rgba(255,180,172,0.2)).

### Input Fields: The Recessed Ledger
*   **Style:** Background `surface-container-lowest`. No bottom border.
*   **Indicator:** A 2px vertical "notch" of `primary` on the left side only when the field is focused.
*   **Typography:** Labels must use `label-sm` in `on_surface_variant` (Ochre-tinted) to differentiate from user-entered data.

### Lists & Tables: The Borderless Data
*   **Forbid Dividers:** Do not use horizontal lines between rows.
*   **Alternating Tones:** Use `surface-container-low` for even rows and `surface-container-lowest` for odd rows.
*   **Padding:** Extreme vertical padding (`spacing.4`) to give data room to "breathe."

### Additional Component: The "Attendance Pulse"
A custom visualization component for educational tracking. Use a sparkline with a `primary` to `primary_fixed` gradient, sitting on a `surface_container_high` background. No axes, no grid lines—only the data.

---

## 6. Do’s and Don’ts

### Do
*   **Do** use `spacing.12` (4rem) for page margins to create a high-end editorial feel.
*   **Do** use Lucide icons with `stroke-width: 1.5px` and `rounded corners` for a softened, premium look.
*   **Do** nest containers to create depth (e.g., a "Highest" container inside a "Low" container).

### Don't
*   **Don't** use pure white (#FFFFFF) for body text. Use `on_surface` (#e3e2e3) to reduce eye strain in dark mode.
*   **Don't** use 100% opaque borders. They clutter the UI and break the "Vault" aesthetic.
*   **Don't** use standard "drop shadows" with 0 blur. If it’s not soft and ambient, it doesn’t belong in the ledger.