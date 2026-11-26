# Manual da rotina diária "Alcance grátis" — Gestor Dental PRO

Objetivo: trazer dentistas para o Gestor Dental PRO **sem gastar com anúncios**, por dois caminhos:
1. **Google (SEO):** 1 artigo novo por dia no blog `dental.aastecnologiaeditorial.com.br/blog/`, respondendo dúvidas que dentistas pesquisam.
2. **Prospecção manual do dia:** uma lista curta de consultórios reais para o Alisson abordar **ele mesmo**, com mensagens prontas.

## Parte 1 — Artigo do dia

1. Leia `_automacao/blog/posts/*.json` para saber o que já foi publicado. **Nunca repita tema nem palavra-chave.**
2. Escolha o próximo tema da **Pauta** abaixo, que ainda não foi usado, em ordem. Se a pauta acabar, crie um tema novo no mesmo estilo (dúvida real de dentista sobre gestão, finanças, agenda, pacientes ou documentos) e acrescente-o à pauta.
3. Escreva o JSON em `_automacao/blog/posts/<slug>.json` com os campos:
   - `slug`: só letras minúsculas, números e hífens (ex.: `como-reduzir-faltas-consultorio-odontologico`).
   - `titulo`: até 70 caracteres, com a palavra-chave no começo, em forma de pergunta ou promessa clara.
   - `descricao`: 140 a 160 caracteres, para aparecer no Google.
   - `data`: hoje (AAAA-MM-DD, fuso America/Sao_Paulo).
   - `palavra_chave`: a busca principal.
   - `cta`: `mercado` (temas de preço/lucro), `diagnostico` (faltas, orçamentos, inadimplência, caixa) ou `demo` (os demais).
   - `corpo_md`: 900 a 1.400 palavras. Use `##` para seções, `###` para subseções, listas com `-` ou `1.`, `**negrito**` e `> ` para exemplos. Pelo menos 1 exemplo com números calculados corretamente (confira a conta em Python antes). Termine com "Resumo" em lista.
4. Rode `python3 _automacao/blog.py` (gera a página, a lista do blog, o `sitemap.xml` e o `robots.txt`). Abra o HTML gerado e confira se está correto.
5. Faça commit e push para `main` (autor `Alisson0408 <as9720476@gmail.com>`). Só altere: `_automacao/blog/`, `_automacao/BLOG.md` (pauta/registro), `blog/`, `sitemap.xml`, `robots.txt`.

### Regras de conteúdo (obrigatórias)
- Escreva em português do Brasil, tom de colega experiente, frases curtas, prático. O leitor é **dentista dono de consultório**.
- **Nunca** invente estatísticas, pesquisas, clientes, depoimentos, resultados ou números de usuários do sistema. Exemplos numéricos devem ser apresentados como exemplo ("imagine um consultório com…").
- Nada de promessa de resultado garantido. Nada de orientação clínica (diagnóstico, tratamento, doses). Em temas legais/éticos (CFO, LGPD, receituário, prontuário, publicidade), seja conservador, cite a norma só se tiver certeza e recomende confirmar com o CRO/contador/advogado.
- Pode citar funções que **realmente existem** no sistema: agenda com confirmação por WhatsApp, lista de espera, follow-up de orçamentos, contas a receber e lembretes de pagamento, previsão de caixa, convênios e glosas, retorno de pacientes, estoque, custos e preços, Análise de mercado, prontuário com odontograma/anamnese/evolução, documentos (anamnese, plano, TCLE, LGPD, receituário, atestado, declaração de comparecimento, pedido de exame/encaminhamento, orientações pós-operatórias), equipe com perfis. Não cite funções que não estão nessa lista.
- Mencione o sistema no máximo 2 vezes no corpo; o bloco de chamada no final já é gerado automaticamente.

## Parte 2 — Prospecção do dia (para o Alisson enviar à mão)

- Pegue a próxima cidade da lista **Cidades** abaixo (a primeira sem data). Marque a data de hoje ao lado dela.
- Com a busca na web, encontre **até 10 consultórios ou dentistas autônomos** dessa cidade com contato **comercial público** (site, perfil do Instagram do consultório ou WhatsApp divulgado publicamente para a clínica). Prefira consultórios pequenos (1 a 3 dentistas).
- **Não** grave nomes, telefones ou perfis neste repositório (ele é público). Eles vão só na mensagem final para o Alisson.
- Para cada um, entregue: nome do consultório, cidade, onde achou (link), e uma **mensagem curta e personalizada** (até 350 caracteres) que cite algo verdadeiro do perfil/site deles, ofereça valor grátis (o diagnóstico em `/comecar/` ou o artigo do dia) e não pareça spam. Sem links encurtados, sem pressão, sem "promoção por tempo limitado".
- Lembre ao Alisson no fim: enviar no máximo 20 a 30 mensagens por dia pelo WhatsApp Business do 019 ou pelo direct do @gestordentalpro, sempre à mão, para não arriscar bloqueio.

## Pauta (marque com a data quando publicar)
1. Como calcular o preço de um procedimento odontológico — 2026-11-25
2. Como reduzir faltas no consultório odontológico — 2026-11-26
3. Mensagem de confirmação de consulta pelo WhatsApp: modelos que funcionam
4. Follow-up de orçamento odontológico: quando e como retomar o paciente
5. Como cobrar paciente inadimplente sem constrangimento
6. Custo da hora clínica: como calcular e por que ele muda tudo
7. Vale a pena atender convênio odontológico? Como fazer a conta
8. Glosa em convênio odontológico: principais motivos e como evitar
9. Fluxo de caixa do consultório odontológico: como prever o mês
10. Quanto cobrar por uma restauração em resina
11. Quanto cobrar por um tratamento de canal
12. Quanto cobrar por um implante dentário
13. Como montar a tabela de preços do consultório
14. Prontuário odontológico: o que precisa ter e por quanto tempo guardar
15. Termo de consentimento (TCLE) na odontologia: para que serve
16. LGPD no consultório odontológico: o básico que todo dentista precisa fazer
17. Atestado odontológico: como emitir corretamente
18. Receituário odontológico: tipos de receita que o dentista emite
19. Como aumentar a taxa de aprovação de orçamentos
20. Parcelamento de tratamento odontológico: como oferecer sem perder dinheiro
21. Como trazer de volta pacientes que sumiram (retorno e recall)
22. Lista de espera: como preencher horários vagos na agenda
23. Controle de estoque no consultório odontológico
24. Indicadores que todo consultório odontológico deveria acompanhar
25. Planilha ou sistema para consultório odontológico? Prós e contras
26. Como precificar prótese considerando o custo do laboratório
27. Como definir o pró-labore do dentista dono do consultório
28. Comissão de dentista: como calcular o repasse sem prejudicar a clínica
29. Como organizar a recepção do consultório odontológico
30. Primeira consulta odontológica: como converter avaliação em tratamento

## Cidades (marque com a data quando usar)
Uberlândia (MG) · Uberaba (MG) · Araguari (MG) · Patos de Minas (MG) · Ituiutaba (MG) · Campinas (SP) · Piracicaba (SP) · Limeira (SP) · Americana (SP) · Sumaré (SP) · Jundiaí (SP) · Ribeirão Preto (SP) · Franca (SP) · São José do Rio Preto (SP) · Goiânia (GO) · Anápolis (GO) · Belo Horizonte (MG) · Contagem (MG) · Juiz de Fora (MG) · Montes Claros (MG) · Londrina (PR) · Maringá (PR) · Curitiba (PR) · Campo Grande (MS) · Brasília (DF)

Registro de uso das cidades (uma por linha, `Cidade — AAAA-MM-DD`):
Uberlândia (MG) — 2026-11-26
