import styles from './SpecialThanks.module.css'

const contributors = [
  {
    name: 'Sir Faisal Hayat',
    contribution: 'For exceptional guidance and mentorship throughout the project, inspiring us to achieve excellence in AI and machine learning.',
  },
  {
    name: 'Sir Atta Ullah',
    contribution: 'For invaluable support and technical expertise, helping us build a robust and scalable solution.',
  },
]

export default function SpecialThanks() {
  return (
    <section className={styles.specialThanks}>
      <div className={styles.container}>
        <h2 className={styles.heading}>Special Thanks</h2>
        <p className={styles.intro}>
          We would like to extend our heartfelt gratitude to these exceptional individuals
        </p>
        <div className={styles.grid}>
          {contributors.map((contributor, index) => (
            <div key={index} className={styles.card}>
              <div className={styles.icon}>⭐</div>
              <h3 className={styles.name}>{contributor.name}</h3>
              <p className={styles.contribution}>{contributor.contribution}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
