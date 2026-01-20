import styles from './Hero.module.css'

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
          <button className={styles.cta}>
            Get Started
          </button>
        </div>
      </div>
    </section>
  )
}
