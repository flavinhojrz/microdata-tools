import type { Metadata } from "next"
import { Heart } from "lucide-react"
import { DocSection, DocShell } from "@/components/doc-shell"

export const metadata: Metadata = {
  title: "Apoiar — MicroData Tools",
  description:
    "O MicroData Tools é gratuito. Doações ajudam a manter a hospedagem, melhorias e novos recursos.",
}

const DONATE_URL = "https://buymeacoffee.com/flavinhojr"

const supportItems = [
  "Hospedagem do frontend e do backend",
  "Testes e correções",
  "Melhorias na ferramenta e na experiência",
  "Aumentar o limite de tamanho dos arquivos",
  "Novos formatos de conversão",
  "Novos relatórios e análises",
]

export default function DonatePage() {
  return (
    <DocShell
      title="Apoiar o projeto"
      intro="O MicroData Tools é e continua gratuito. Se ele te ajuda, uma doação ajuda a mantê-lo no ar e a evoluir."
    >
      <DocSection title="Por que apoiar">
        <p>
          Não há cobrança, login ou plano pago. As doações são voluntárias e
          ajudam a cobrir os custos de hospedagem, financiar melhorias e
          viabilizar novos recursos ao longo do tempo.
        </p>
        <div className="flex flex-col items-start gap-4 pt-1">
          <a
            href={DONATE_URL}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 rounded-md bg-primary px-4 py-2.5 text-sm font-medium text-primary-foreground transition-opacity hover:opacity-90"
          >
            <Heart className="size-4" strokeWidth={1.5} />
            Apoiar projeto
          </a>
          <a
            href={DONATE_URL}
            target="_blank"
            rel="noopener noreferrer"
            aria-label="Buy me a coffee"
            className="transition-opacity hover:opacity-90"
          >
            {/* Botão oficial do Buy Me a Coffee (imagem hospedada pela própria plataforma). */}
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img
              src="https://img.buymeacoffee.com/button-api/?text=Buy me a coffee&emoji=&slug=flavinhojr&button_colour=5F7FFF&font_colour=ffffff&font_family=Inter&outline_colour=000000&coffee_colour=FFDD00"
              alt="Buy me a coffee"
              className="h-[60px] w-auto"
            />
          </a>
        </div>
      </DocSection>

      <DocSection title="Para onde vai o apoio?">
        <p>O que entra é reinvestido diretamente no projeto:</p>
        <ul className="flex list-disc flex-col gap-1.5 pl-5">
          {supportItems.map((item) => (
            <li key={item}>{item}</li>
          ))}
        </ul>
      </DocSection>

      <DocSection title="Sobre o pagamento">
        <p>
          O pagamento é feito fora da ferramenta, na plataforma de doação. O
          MicroData Tools não processa pagamentos e não coleta nenhum dado de
          cartão ou cobrança.
        </p>
      </DocSection>
    </DocShell>
  )
}
