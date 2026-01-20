# V2T Component Documentation

## 📚 Component Overview

This document provides detailed information about each component in the V2T frontend application.

---

## 🧩 Components

### 1. Header (`components/Header.tsx`)

**Purpose**: Sticky navigation bar with responsive menu

**Features**:
- Sticky positioning (stays at top while scrolling)
- Smooth scroll navigation to sections
- Responsive hamburger menu for mobile
- Authentication buttons (Sign In / Sign Up)

**Props**: None (self-contained)

**State**:
- `isMenuOpen`: Boolean - Controls mobile menu visibility

**Key Functions**:
- `toggleMenu()`: Opens/closes mobile menu
- `scrollToSection(id)`: Smooth scrolls to section

**Styling**: [Header.module.css](components/Header.module.css)

**Customization**:
```tsx
// Change navigation links
<button onClick={() => scrollToSection('new-section')}>
  New Link
</button>
```

---

### 2. Hero (`components/Hero.tsx`)

**Purpose**: Eye-catching landing section with CTA

**Features**:
- Gradient background with pattern overlay
- Responsive text sizing
- Call-to-action button
- Text shadow for readability

**Props**: None

**Styling**: [Hero.module.css](components/Hero.module.css)

**Customization**:
```tsx
// Change heading
<h1>Your New Heading</h1>

// Change CTA link
<button onClick={() => router.push('/upload')}>
  Get Started
</button>
```

---

### 3. Team (`components/Team.tsx`)

**Purpose**: Showcase team members in cards

**Features**:
- Responsive grid layout (1-4 columns)
- Avatar with initials
- Hover effects with elevation
- Dynamic team member rendering

**Props**: None

**Data Structure**:
```typescript
{
  name: string,
  role: string,
  description: string
}
```

**Styling**: [Team.module.css](components/Team.module.css)

**Customization**:
```tsx
// Add new team member
const teamMembers = [
  ...existing,
  {
    name: 'New Member',
    role: 'Position',
    description: 'Bio'
  }
]
```

---

### 4. SpecialThanks (`components/SpecialThanks.tsx`)

**Purpose**: Recognition section for contributors

**Features**:
- Animated star icons (pulse effect)
- Gradient background
- Two-column responsive layout
- Top border accent

**Props**: None

**Data Structure**:
```typescript
{
  name: string,
  contribution: string
}
```

**Styling**: [SpecialThanks.module.css](components/SpecialThanks.module.css)

---

### 5. Contact (`components/Contact.tsx`)

**Purpose**: Contact form with validation

**Features**:
- Client-side form validation
- Loading states
- Success/error messages
- Email integration ready

**Props**: None

**State**:
- `formData`: Object with name, email, message
- `status`: 'sending' | 'success' | 'error' | ''

**Key Functions**:
- `handleChange(e)`: Updates form fields
- `handleSubmit(e)`: Processes form submission

**Styling**: [Contact.module.css](components/Contact.module.css)

**Backend Integration**:
```typescript
// Replace simulation with real API
const response = await axios.post('/api/contact', formData)
```

---

### 6. Footer (`components/Footer.tsx`)

**Purpose**: Site footer with links and social media

**Features**:
- Four-column responsive grid
- Social media icons (SVG)
- Copyright with dynamic year
- Dark theme

**Props**: None

**Styling**: [Footer.module.css](components/Footer.module.css)

**Customization**:
```tsx
// Add new social link
<a href="https://instagram.com" className={styles.socialIcon}>
  <svg>...</svg>
</a>
```

---

## 🎨 Styling System

### CSS Modules

All components use CSS Modules for scoped styling:
- Prevents style conflicts
- Component-specific classes
- Better maintainability

### CSS Variables

Global variables in [app/globals.css](app/globals.css):

```css
:root {
  --primary-blue: #8bb7d4;
  --secondary-white: #f4f4f4;
  --accent-blue: #4b7e8e;
  --dark-blue: #3a5f6b;
  --text-dark: #333333;
  --shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  --shadow-hover: 0 4px 12px rgba(0, 0, 0, 0.15);
}
```

### Common Patterns

**Hover Effects**:
```css
.element {
  transition: all 0.3s ease;
}

.element:hover {
  transform: translateY(-5px);
  box-shadow: var(--shadow-hover);
}
```

**Responsive Breakpoints**:
```css
@media (max-width: 768px) { /* Tablet */ }
@media (max-width: 480px) { /* Mobile */ }
```

---

## 📱 Responsive Design

### Breakpoints

- **Desktop**: > 768px - Full layout
- **Tablet**: 480px - 768px - Adjusted grids
- **Mobile**: < 480px - Stacked layout

### Mobile Menu

The Header component implements a hamburger menu:
- Slides in from left
- Overlay navigation
- Animated hamburger icon
- Closes on link click

---

## 🔧 Component Guidelines

### Creating New Components

1. **Create component file**:
   ```tsx
   // components/NewComponent.tsx
   export default function NewComponent() {
     return <div>Content</div>
   }
   ```

2. **Create CSS module**:
   ```css
   /* components/NewComponent.module.css */
   .container { /* styles */ }
   ```

3. **Import in page**:
   ```tsx
   import NewComponent from '@/components/NewComponent'
   ```

### Best Practices

- ✅ Use TypeScript for type safety
- ✅ Use CSS Modules for styling
- ✅ Keep components small and focused
- ✅ Use semantic HTML
- ✅ Add accessibility attributes
- ✅ Make responsive by default
- ✅ Use CSS variables for colors

---

## 🎯 Component Hierarchy

```
app/page.tsx (Home Page)
├── Header
├── Hero
├── Team
├── SpecialThanks
├── Contact
└── Footer
```

---

## 🔄 State Management

Currently using local component state with `useState`.

For larger applications, consider:
- **Context API** - For global state
- **Zustand** - Lightweight state management
- **Redux Toolkit** - Complex state needs

---

## 🧪 Testing Components

### Manual Testing Checklist

- [ ] Desktop view (> 768px)
- [ ] Tablet view (480-768px)
- [ ] Mobile view (< 480px)
- [ ] Hover states work
- [ ] Buttons are clickable
- [ ] Forms validate properly
- [ ] Navigation scrolls smoothly
- [ ] Mobile menu opens/closes

### Automated Testing (Future)

```bash
npm install --save-dev @testing-library/react
```

---

## 📊 Performance Tips

1. **Lazy Loading**: Use Next.js dynamic imports
2. **Image Optimization**: Use `next/image`
3. **Code Splitting**: Automatic in Next.js
4. **Memoization**: Use `React.memo` for expensive renders

---

## 🐛 Common Issues

### Component Not Rendering
- Check import path
- Verify component export
- Check console for errors

### Styles Not Applying
- Ensure CSS Module import
- Check class name spelling
- Verify CSS variable exists

### Mobile Menu Not Working
- Check `isMenuOpen` state
- Verify button onClick handler
- Check CSS transitions

---

## 📚 Additional Resources

- [Next.js Documentation](https://nextjs.org/docs)
- [React Documentation](https://react.dev)
- [CSS Modules Guide](https://github.com/css-modules/css-modules)
- [Material-UI Components](https://mui.com)

---

Made with ❤️ by the V2T Team
