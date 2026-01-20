# V2T Frontend - Quick Start Guide

## 🚀 Getting Started in 3 Steps

### Step 1: Install Dependencies
```bash
npm install
```

This will install all required packages including:
- Next.js 14
- React 18
- Material-UI
- Axios
- TypeScript

### Step 2: Run Development Server
```bash
npm run dev
```

The application will start at [http://localhost:3000](http://localhost:3000)

### Step 3: Open in Browser
Navigate to `http://localhost:3000` to see your V2T application!

---

## 📋 What You'll See

### 1. **Header** (Sticky Navigation)
- V2T logo on the left
- Navigation links: Home, Team, Contact Us
- Sign In / Sign Up buttons
- Responsive hamburger menu on mobile

### 2. **Hero Section**
- Eye-catching gradient background
- Main heading: "Extract Text from Videos with Advanced AI"
- Call-to-action button: "Get Started"

### 3. **Team Section**
- 6 team member cards with avatars
- Names and roles displayed
- Hover effects for interactivity

### 4. **Special Thanks Section**
- Recognition for Sir Faisal Hayat
- Recognition for Sir Atta Ullah
- Animated star icons

### 5. **Contact Form**
- Name input field
- Email input field
- Message textarea
- Submit button with loading state

### 6. **Footer**
- About V2T
- Quick links
- Legal links (Privacy Policy, Terms)
- Social media icons (LinkedIn, GitHub, Twitter)

---

## 🎨 Customization Tips

### Change Colors
Edit [app/globals.css](app/globals.css):
```css
:root {
  --primary-blue: #8bb7d4;      /* Main brand color */
  --secondary-white: #f4f4f4;   /* Background */
  --accent-blue: #4b7e8e;       /* Hover states */
  --dark-blue: #3a5f6b;         /* Footer */
}
```

### Update Team Members
Edit [components/Team.tsx](components/Team.tsx) - modify the `teamMembers` array

### Connect to Your Backend
Edit [components/Contact.tsx](components/Contact.tsx):
```typescript
// Replace the simulated API call with:
const response = await axios.post('YOUR_BACKEND_URL/contact', formData)
```

---

## 📱 Test Responsive Design

1. **Desktop**: Full navigation bar
2. **Tablet** (< 768px): Adjusted layouts
3. **Mobile** (< 480px): Hamburger menu, stacked cards

Use browser DevTools to test different screen sizes!

---

## 🔧 Build Commands

```bash
# Development
npm run dev          # Start dev server on localhost:3000

# Production
npm run build        # Build optimized production bundle
npm start           # Start production server

# Linting
npm run lint        # Run ESLint to check code quality
```

---

## 📦 Project Structure Overview

```
V2T Front End/
├── app/                    # Next.js app directory
│   ├── globals.css        # Global styles & CSS variables
│   ├── layout.tsx         # Root layout component
│   └── page.tsx          # Home page (imports all sections)
│
├── components/            # Reusable components
│   ├── Header.*          # Navigation header
│   ├── Hero.*            # Hero section
│   ├── Team.*            # Team showcase
│   ├── SpecialThanks.*   # Recognition section
│   ├── Contact.*         # Contact form
│   └── Footer.*          # Footer
│
├── public/               # Static assets
│   └── favicon.svg      # Site icon
│
├── package.json         # Dependencies
├── next.config.js       # Next.js configuration
└── tsconfig.json        # TypeScript configuration
```

---

## 🎯 Next Steps

1. **Add Images**: Place team member photos in `/public/team/`
2. **Connect Backend**: Update API endpoints in Contact form
3. **Add Auth**: Implement Sign In/Sign Up functionality
4. **Deploy**: Deploy to Vercel, Netlify, or your preferred platform

---

## 🐛 Troubleshooting

### Port Already in Use?
```bash
# Kill process on port 3000
lsof -ti:3000 | xargs kill -9

# Or use a different port
npm run dev -- -p 3001
```

### Module Not Found?
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

### Build Errors?
```bash
# Clean build cache
rm -rf .next
npm run build
```

---

## 📞 Need Help?

Contact the team through the Contact Us section or reach out directly to:
- **Waqas Safdar** - Full Stack Developer

---

Made with ❤️ by the V2T Team
