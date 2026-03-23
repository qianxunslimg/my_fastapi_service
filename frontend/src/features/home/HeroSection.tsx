import { SITE_NAME } from "../../app/constants";

export function HeroSection() {
  return (
    <section className="hero-layout">
      <article className="panel-card hero-primary">
        <p className="eyebrow">{SITE_NAME}</p>
      </article>
    </section>
  );
}
