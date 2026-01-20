# V2T - Video to Text Extraction Frontend

A modern, responsive Next.js application for extracting text from videos using advanced AI technology.

## 🎨 Design Features

- **Color Scheme**
  - Primary Blue: `#8bb7d4`
  - Secondary White/Cream: `#f4f4f4`
  - Accent Blue: `#4b7e8e`
  - Dark Blue: `#3a5f6b`

- **Sections**
  - ✨ Sticky Header with navigation
  - 🚀 Hero section with call-to-action
  - 👥 Team showcase with 6 members
  - ⭐ Special thanks section
  - 📧 Contact form
  - 🔗 Footer with social links

## 🛠️ Tech Stack

- **Next.js 14** - React framework with SSR
- **React 18** - UI library
- **TypeScript** - Type safety
- **CSS Modules** - Scoped styling
- **Material-UI** - UI components
- **Axios** - API requests

## 📦 Installation

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Run development server:**
   ```bash
   npm run dev
   ```

3. **Open your browser:**
   Navigate to [http://localhost:3000](http://localhost:3000)

## 🏗️ Project Structure

```
V2T Front End/
├── app/
│   ├── globals.css          # Global styles
│   ├── layout.tsx           # Root layout
│   └── page.tsx             # Home page
├── components/
│   ├── Header.tsx           # Navigation header
│   ├── Header.module.css
│   ├── Hero.tsx             # Hero section
│   ├── Hero.module.css
│   ├── Team.tsx             # Team showcase
│   ├── Team.module.css
│   ├── SpecialThanks.tsx    # Special thanks
│   ├── SpecialThanks.module.css
│   ├── Contact.tsx          # Contact form
│   ├── Contact.module.css
│   ├── Footer.tsx           # Footer
│   └── Footer.module.css
├── package.json
├── next.config.js
└── tsconfig.json
```

## 👥 Team Members

- **Sir Faisal Hayat** - Instructor
- **Sir Atta Ullah** - Instructor
- **Waqas Safdar** - Full Stack Developer
- **Musab** - Developer
- **Wajid ur Rehman** - Developer
- **Zohaib Ahmad** - Developer

## 📱 Responsive Design

The application is fully responsive with:
- Desktop: Full navigation and multi-column layouts
- Tablet: Adjusted grid layouts
- Mobile: Hamburger menu, stacked layouts

## 🚀 Build for Production

```bash
npm run build
npm start
```

## 🔧 Configuration

The project uses:
- **CSS Variables** for consistent theming
- **CSS Modules** for component-scoped styles
- **TypeScript** for type safety
- **Next.js App Router** for routing

## 🎯 Key Features

1. **Sticky Header** - Always accessible navigation
2. **Smooth Scrolling** - Seamless section navigation
3. **Hover Effects** - Interactive UI elements
4. **Form Validation** - Client-side form validation
5. **Mobile Menu** - Hamburger navigation for mobile
6. **Gradient Backgrounds** - Modern visual design

## 📝 Customization

### Changing Colors

Edit the CSS variables in [app/globals.css](app/globals.css):

```css
:root {
  --primary-blue: #8bb7d4;
  --secondary-white: #f4f4f4;
  --accent-blue: #4b7e8e;
  --dark-blue: #3a5f6b;
}
```

### Adding Team Members

Edit the `teamMembers` array in [components/Team.tsx](components/Team.tsx)

### Connecting to Backend

Update the form submission in [components/Contact.tsx](components/Contact.tsx) to connect to your FastAPI backend:

```typescript
const response = await axios.post('YOUR_API_ENDPOINT', formData)
```

## 📄 License

© 2026 V2T. All rights reserved.

---

Made with ❤️ by the V2T Team
