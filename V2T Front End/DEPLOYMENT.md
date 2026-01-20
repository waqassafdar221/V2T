# V2T Frontend - Deployment Guide

## 🚀 Deployment Options

### 1. Vercel (Recommended for Next.js)

Vercel is the creators of Next.js and offers seamless deployment.

#### Steps:

1. **Install Vercel CLI** (optional):
   ```bash
   npm install -g vercel
   ```

2. **Deploy via CLI**:
   ```bash
   vercel
   ```

3. **Or Deploy via GitHub**:
   - Push your code to GitHub
   - Go to [vercel.com](https://vercel.com)
   - Click "Import Project"
   - Select your repository
   - Vercel will auto-detect Next.js and deploy

#### Environment Variables:
Add these in Vercel Dashboard → Settings → Environment Variables:
```
NEXT_PUBLIC_API_URL=https://your-backend-api.com
```

---

### 2. Netlify

#### Steps:

1. **Build Command**: `npm run build`
2. **Publish Directory**: `.next`
3. **Install Netlify CLI**:
   ```bash
   npm install -g netlify-cli
   ```

4. **Deploy**:
   ```bash
   netlify deploy --prod
   ```

---

### 3. Docker Deployment

#### Create Dockerfile:

```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

EXPOSE 3000

CMD ["npm", "start"]
```

#### Build and Run:

```bash
# Build image
docker build -t v2t-frontend .

# Run container
docker run -p 3000:3000 v2t-frontend
```

---

### 4. AWS Amplify

1. Connect your GitHub repository
2. Amplify auto-detects Next.js
3. Set build settings:
   - Build command: `npm run build`
   - Output directory: `.next`

---

### 5. Traditional VPS (Ubuntu/Debian)

#### Prerequisites:
- Node.js 18+ installed
- Nginx for reverse proxy
- PM2 for process management

#### Steps:

1. **Clone repository**:
   ```bash
   git clone your-repo-url
   cd "V2T Front End"
   ```

2. **Install dependencies**:
   ```bash
   npm install
   npm run build
   ```

3. **Install PM2**:
   ```bash
   npm install -g pm2
   ```

4. **Start with PM2**:
   ```bash
   pm2 start npm --name "v2t-frontend" -- start
   pm2 save
   pm2 startup
   ```

5. **Configure Nginx**:
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           proxy_pass http://localhost:3000;
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection 'upgrade';
           proxy_set_header Host $host;
           proxy_cache_bypass $http_upgrade;
       }
   }
   ```

6. **Enable and restart Nginx**:
   ```bash
   sudo ln -s /etc/nginx/sites-available/v2t /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

---

## 🔒 SSL Certificate (HTTPS)

### Using Let's Encrypt (Free):

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

---

## 📊 Performance Optimization

### Before Deployment:

1. **Optimize Images**: Use Next.js Image component
2. **Enable Compression**: Built into Next.js
3. **Analyze Bundle**: 
   ```bash
   npm install @next/bundle-analyzer
   ```

### In Production:

1. **Enable Caching**: Configure CDN (Cloudflare, AWS CloudFront)
2. **Monitor Performance**: Use Vercel Analytics or Google Analytics
3. **Set up Error Tracking**: Sentry, LogRocket

---

## 🔧 Environment Variables

Create `.env.production`:

```bash
NEXT_PUBLIC_API_URL=https://api.your-domain.com
NEXT_PUBLIC_SITE_URL=https://your-domain.com
```

---

## ✅ Pre-Deployment Checklist

- [ ] Run `npm run build` locally (no errors)
- [ ] Test production build: `npm start`
- [ ] Update environment variables
- [ ] Set up SSL certificate
- [ ] Configure custom domain
- [ ] Set up monitoring/analytics
- [ ] Test on multiple devices
- [ ] Verify API connectivity
- [ ] Check mobile responsiveness
- [ ] Enable error logging

---

## 🐛 Troubleshooting Deployment

### Build Fails:

```bash
# Clear cache
rm -rf .next node_modules
npm install
npm run build
```

### Memory Issues:

```bash
# Increase Node.js memory
NODE_OPTIONS=--max-old-space-size=4096 npm run build
```

### Port Conflicts:

```bash
# Change port in package.json
"start": "next start -p 3001"
```

---

## 📈 Post-Deployment

1. **Monitor Logs**: Check for errors
2. **Test All Features**: Forms, navigation, responsiveness
3. **Set up Analytics**: Google Analytics, Vercel Analytics
4. **Backup**: Regular database and file backups
5. **Updates**: Keep dependencies updated

---

## 🔄 CI/CD Pipeline (GitHub Actions)

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          
      - name: Install dependencies
        run: npm install
        
      - name: Build
        run: npm run build
        
      - name: Deploy to Vercel
        run: vercel --prod
        env:
          VERCEL_TOKEN: ${{ secrets.VERCEL_TOKEN }}
```

---

## 📞 Support

For deployment issues, contact:
- **Waqas Safdar** - Full Stack Developer

---

Happy Deploying! 🚀
