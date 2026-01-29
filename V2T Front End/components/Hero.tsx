import styles from './Hero.module.css'
import Link from 'next/link'

export default function Hero() {
  return (
    <section id="home" className={styles.hero}>
      <div className={styles.overlay}>
        <div className={styles.container}>
          <h1 className={styles.heading}>
            Extract Text from Videos with Advanced AI
          </h1>
          <p className={styles.subheading}>
            Leverage AI to extract meaningful text and insights from videos with just a few clicks
          </p>
          <Link href="/auth/signup">
            <button className={styles.cta}>
              Get Started
            </button>
          </Link>
        </div>
      </div>
    </section>
  )
}
