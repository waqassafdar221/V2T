import styles from './Team.module.css'

const teamMembers = [
  {
    name: 'Sir Faisal Hayat',
    role: 'Instructor',
    description: 'Leading the team with expertise in AI and machine learning, guiding the development of cutting-edge solutions.',
  },
  {
    name: 'Sir Atta Ullah',
    role: 'Instructor',
    description: 'Providing valuable insights and mentorship in software architecture and best practices.',
  },
  {
    name: 'Waqas Safdar',
    role: 'Full Stack Developer',
    description: 'Building robust frontend and backend systems to deliver seamless user experiences.',
  },
  {
    name: 'Musab',
    role: 'Developer',
    description: 'Contributing to the development of innovative features and ensuring code quality.',
  },
  {
    name: 'Wajid ur Rehman',
    role: 'Developer',
    description: 'Focused on implementing efficient algorithms and optimizing system performance.',
  },
  {
    name: 'Zohaib Ahmad',
    role: 'Developer',
    description: 'Working on video processing and AI integration to enhance extraction accuracy.',
  },
]

export default function Team() {
  return (
    <section id="team" className={styles.team}>
      <div className={styles.container}>
        <h2 className={styles.heading}>Our Team</h2>
        <p className={styles.subheading}>
          Meet the talented individuals behind V2T
        </p>
        <div className={styles.grid}>
          {teamMembers.map((member, index) => (
            <div key={index} className={styles.card}>
              <div className={styles.avatar}>
                <span className={styles.initials}>
                  {member.name.split(' ').map(n => n[0]).join('').substring(0, 2)}
                </span>
              </div>
              <h3 className={styles.name}>{member.name}</h3>
              <p className={styles.role}>{member.role}</p>
              <p className={styles.description}>{member.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
