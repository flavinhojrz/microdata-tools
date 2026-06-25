const footerLinks = [
  { label: "Apoiar projeto", href: "#apoiar" },
  { label: "Privacidade", href: "#privacidade" },
  { label: "GitHub", href: "#" },
]

export function Footer() {
  return (
    <footer
      id="privacidade"
      className="mt-20 border-t border-border"
    >
      <div className="mx-auto flex max-w-6xl flex-col gap-4 px-5 py-8 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <p className="text-sm font-medium">MicroData Tools</p>
          <p className="mt-0.5 text-xs text-muted-foreground">
            Ferramenta gratuita para dados simples.
          </p>
        </div>
        <nav className="flex flex-wrap gap-x-6 gap-y-2">
          {footerLinks.map((link) => (
            <a
              key={link.label}
              href={link.href}
              className="text-sm text-muted-foreground transition-colors hover:text-foreground"
            >
              {link.label}
            </a>
          ))}
        </nav>
      </div>
    </footer>
  )
}
