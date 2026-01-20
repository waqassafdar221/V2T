# 🎨 V2T Style Guide

## Color Palette

### Primary Colors

```
┌─────────────────────────────────────┐
│  Primary Blue (#8bb7d4)             │
│  Main brand color                   │
│  Used for: Headers, buttons, links  │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│  Off-White (#f4f4f4)                │
│  Background color                   │
│  Used for: Backgrounds, light text  │
└─────────────────────────────────────┘
```

### Accent Colors

```
┌─────────────────────────────────────┐
│  Accent Blue (#4b7e8e)              │
│  Darker shade for emphasis          │
│  Used for: Hover states, CTAs       │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│  Dark Blue (#3a5f6b)                │
│  Darkest shade                      │
│  Used for: Footer, dark sections    │
└─────────────────────────────────────┘
```

### Text Colors

```
Text Dark (#333333) - Main body text
Off-White (#f4f4f4) - Text on dark backgrounds
Primary Blue (#8bb7d4) - Headings and links
```

---

## Typography

### Font Family
**Primary**: Roboto (Google Fonts)
- Light (300)
- Regular (400)
- Medium (500)
- Bold (700)

### Font Sizes

```
h1: 3.5rem (56px)   - Hero heading
h2: 2.8rem (44.8px) - Section headings
h3: 1.6rem (25.6px) - Card titles
h4: 1.2rem (19.2px) - Subsection titles
p:  1rem (16px)     - Body text
small: 0.9rem       - Footer text
```

### Line Heights

```
Headings: 1.2
Body text: 1.6
Descriptions: 1.7
```

---

## Spacing System

```
Section Padding: 80px (top/bottom)
Container Padding: 20px (left/right)
Card Padding: 2rem
Button Padding: 1rem 3rem
Input Padding: 0.9rem 1rem
```

### Margins

```
Heading margin-bottom: 1rem - 1.5rem
Paragraph margin-bottom: 1rem
Section margin-bottom: 3rem
```

---

## Shadows

```css
/* Light Shadow */
--shadow: 0 2px 8px rgba(0, 0, 0, 0.1);

/* Hover Shadow */
--shadow-hover: 0 4px 12px rgba(0, 0, 0, 0.15);

/* Card Hover */
box-shadow: 0 8px 24px rgba(139, 183, 212, 0.4);
```

---

## Border Radius

```
Small elements: 4px - 8px
Cards: 12px - 16px
Buttons: 25px - 50px (rounded)
Avatars: 50% (circle)
```

---

## Buttons

### Primary Button
```
Background: #8bb7d4
Color: #f4f4f4
Padding: 1rem 3rem
Border-radius: 50px
Hover: Darker blue + lift effect
```

### Secondary Button
```
Background: transparent
Color: #f4f4f4
Border: 2px solid #f4f4f4
Padding: 0.6rem 1.5rem
Border-radius: 25px
Hover: Filled background
```

### Example Usage
```tsx
<button className="primary">Get Started</button>
<button className="secondary">Sign In</button>
```

---

## Cards

### Team Cards
```
Background: white
Padding: 2rem
Border-radius: 12px
Shadow: var(--shadow)
Hover: translateY(-8px) + border
```

### Special Thanks Cards
```
Background: white
Padding: 3rem 2rem
Border-radius: 16px
Border-top: 4px gradient
```

---

## Forms

### Input Fields
```
Background: #f4f4f4
Border: 2px solid #ddd
Border-radius: 8px
Padding: 0.9rem 1rem
Focus: Blue border + shadow
```

### Textarea
```
Min-height: 120px
Resize: vertical
Same styling as input
```

### Labels
```
Font-weight: 600
Margin-bottom: 0.5rem
Color: #333333
```

---

## Grid Layouts

### Team Section
```
Desktop: 3-4 columns
Tablet: 2 columns
Mobile: 1 column
Gap: 2rem
```

### Footer
```
Desktop: 4 columns
Tablet: 2 columns
Mobile: 1 column
```

---

## Animations

### Hover Effects
```css
transition: all 0.3s ease;

/* Lift Effect */
transform: translateY(-3px);

/* Scale Effect */
transform: scale(1.05);
```

### Pulse Animation (Special Thanks)
```css
@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.1); }
}
```

---

## Responsive Breakpoints

```
Desktop:  > 768px
Tablet:   480px - 768px
Mobile:   < 480px
```

### Media Queries
```css
@media (max-width: 768px) {
  /* Tablet styles */
}

@media (max-width: 480px) {
  /* Mobile styles */
}
```

---

## Icons & Symbols

### Social Media Icons
- Size: 24px × 24px
- Color: #f4f4f4
- Hover: #8bb7d4

### Special Thanks Icon
- Emoji: ⭐
- Size: 3rem
- Animation: pulse

---

## Gradients

### Hero Background
```css
background: linear-gradient(135deg, 
  var(--primary-blue) 0%, 
  var(--accent-blue) 100%
);
```

### Special Thanks Background
```css
background: linear-gradient(135deg, 
  var(--secondary-white) 0%, 
  #e8f4f8 100%
);
```

---

## Component-Specific Styles

### Header
- Height: Auto (sticky)
- Background: #8bb7d4
- Z-index: 1000
- Shadow: var(--shadow)

### Hero
- Min-height: 600px
- Pattern overlay: Subtle dots
- Text shadow: 2px 2px 4px rgba(0,0,0,0.2)

### Footer
- Background: #3a5f6b
- Color: #f4f4f4
- Padding: 60px 20px 30px

---

## Accessibility

### Focus States
```css
:focus {
  outline: 2px solid var(--primary-blue);
  outline-offset: 2px;
}
```

### Color Contrast
All text meets WCAG AA standards:
- Dark text on light backgrounds
- Light text on dark backgrounds

### Interactive Elements
- Min touch target: 44px × 44px
- Clear hover states
- Keyboard navigation support

---

## Code Examples

### Using CSS Variables
```tsx
<div style={{ 
  backgroundColor: 'var(--primary-blue)',
  color: 'var(--secondary-white)'
}}>
  Content
</div>
```

### Applying Hover Effect
```css
.card {
  transition: all 0.3s ease;
}

.card:hover {
  transform: translateY(-8px);
  box-shadow: var(--shadow-hover);
}
```

---

## Design Principles

1. **Consistency**: Use design tokens (CSS variables)
2. **Simplicity**: Clean, minimal design
3. **Responsiveness**: Mobile-first approach
4. **Accessibility**: WCAG compliant
5. **Performance**: Optimized CSS
6. **Maintainability**: CSS Modules

---

## Quick Reference

### Common Patterns

**Card**:
- White background
- 2rem padding
- 12px border radius
- Subtle shadow
- Hover: lift + border

**Button**:
- Primary blue background
- White text
- Rounded (50px)
- Hover: darker + lift

**Section**:
- 80px vertical padding
- Max-width 1200px
- Centered container

---

## Tools & Resources

- **Color Picker**: [Coolors.co](https://coolors.co)
- **Gradient Generator**: [CSS Gradient](https://cssgradient.io)
- **Shadow Generator**: [Box Shadow CSS](https://box-shadow.dev)
- **Font Pairing**: [Google Fonts](https://fonts.google.com)

---

Made with ❤️ by the V2T Team
