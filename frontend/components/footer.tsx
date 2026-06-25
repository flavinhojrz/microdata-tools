import Link from "next/link"

const footerLinks = [
  { label: "Apoiar projeto", href: "/donate", external: false },
  { label: "Privacidade", href: "/privacy", external: false },
  {
    label: "GitHub",
    href: "https://github.com/flavinhojrz/microdata-tools",
    external: true,
  },
]

export function Footer() {
  return (
    <footer className="mt-20 border-t border-border">
      <div className="mx-auto flex max-w-6xl flex-col gap-4 px-5 py-8 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <p className="text-sm font-medium">MicroData Tools</p>
          <p className="mt-0.5 text-xs text-muted-foreground">
            Ferramenta gratuita para dados simples.
          </p>
        </div>
        <nav className="flex flex-wrap gap-x-6 gap-y-2">
          {footerLinks.map((link) =>
            link.external ? (
              <a
                key={link.label}
                href={link.href}
                target="_blank"
                rel="noopener noreferrer"
                className="text-sm text-muted-foreground transition-colors hover:text-foreground"
              >
                {link.label}
              </a>
            ) : (
              <Link
                key={link.label}
                href={link.href}
                className="text-sm text-muted-foreground transition-colors hover:text-foreground"
              >
                {link.label}
              </Link>
            ),
          )}
        </nav>
      </div>
    </footer>
  )
}
