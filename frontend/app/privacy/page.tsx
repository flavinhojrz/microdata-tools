import type { Metadata } from "next"
import { DocSection, DocShell } from "@/components/doc-shell"

export const metadata: Metadata = {
  title: "Privacidade — MicroData Tools",
  description:
    "Como o MicroData Tools trata os arquivos enviados: processamento em memória, sem armazenamento permanente e sem uso para treinar IA.",
}

export default function PrivacyPage() {
  return (
    <DocShell
      title="Privacidade"
      intro="Esta página explica, em linguagem simples, como o MicroData Tools trata os arquivos que você envia. Sem juridiquês."
      meta="Última atualização: 25 de junho de 2026"
    >
      <DocSection title="O que é o MicroData Tools">
        <p>
          O MicroData Tools é uma ferramenta gratuita para limpar, converter e
          analisar planilhas CSV e Excel. Não exige login, não cria conta e não
          mantém um histórico do que você processa.
        </p>
      </DocSection>

      <DocSection title="O que acontece com seus arquivos">
        <p>
          Quando você usa a ferramenta, o arquivo é enviado para o nosso servidor
          para processamento. Ele é usado apenas para gerar o resultado que você
          pediu: prévia, limpeza, conversão e análise.
        </p>
        <p>
          O processamento acontece em memória e o arquivo{" "}
          <strong className="font-medium text-foreground">
            não é armazenado de forma permanente
          </strong>
          . Não guardamos os arquivos enviados nem os resultados gerados após
          devolver a resposta para você.
        </p>
        <p>
          Também{" "}
          <strong className="font-medium text-foreground">
            não usamos seus arquivos para treinar inteligência artificial
          </strong>{" "}
          nem para qualquer finalidade além de gerar o resultado solicitado.
        </p>
      </DocSection>

      <DocSection title="Logs técnicos">
        <p>
          Para manter o serviço no ar e diagnosticar problemas, os servidores
          podem registrar logs técnicos. Esses logs podem incluir o seu endereço
          IP, a rota acessada, o horário do acesso, o user-agent (navegador) e
          mensagens de erro.
        </p>
        <p>
          Esses registros servem para operação e segurança e não incluem o
          conteúdo das suas planilhas.
        </p>
      </DocSection>

      <DocSection title="Dados sensíveis">
        <p>
          Evite enviar dados extremamente sensíveis, como documentos de
          identidade, dados bancários completos, senhas ou informações de saúde.
          A ferramenta foi feita para planilhas do dia a dia, e você é quem
          decide o que enviar.
        </p>
      </DocSection>

      <DocSection title="Serviços de terceiros">
        <p>Usamos dois serviços de hospedagem para manter a ferramenta no ar:</p>
        <ul className="flex list-disc flex-col gap-1.5 pl-5">
          <li>
            <strong className="font-medium text-foreground">Vercel</strong> —
            hospeda o frontend (a interface que você usa no navegador).
          </li>
          <li>
            <strong className="font-medium text-foreground">Render</strong> —
            hospeda o backend (que processa os arquivos).
          </li>
        </ul>
        <p>
          Ao usar a ferramenta, o tráfego passa por esses provedores, que têm
          suas próprias políticas de privacidade.
        </p>
      </DocSection>

      <DocSection title="Contato">
        <p>
          Dúvidas sobre privacidade? Fale com a gente em{" "}
          <a
            href="mailto:flavinhoolvs@gmail.com"
            className="text-foreground underline underline-offset-4"
          >
            flavinhoolvs@gmail.com
          </a>
          .
        </p>
      </DocSection>

      <DocSection title="Importante">
        <p>
          Trabalhamos para tratar seus dados com cuidado, mas nenhuma ferramenta
          on-line pode prometer segurança absoluta. Use a ferramenta com bom
          senso sobre o que envia.
        </p>
      </DocSection>
    </DocShell>
  )
}
