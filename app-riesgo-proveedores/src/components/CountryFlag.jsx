export default function CountryFlag({ alpha2, alt = '' }) {
  if (!alpha2 || alpha2.length !== 2) return null
  return (
    <img
      className="flag"
      src={`https://flagcdn.com/w40/${alpha2.toLowerCase()}.png`}
      alt={alt}
      loading="lazy"
    />
  )
}
