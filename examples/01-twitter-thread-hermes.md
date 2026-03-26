# Example 01 — Twitter/X Thread with Hermes

## Prompt to the agent

```
Investigá qué está pasando con inteligencia artificial esta semana y generame un hilo viral de Twitter en español.
```

## What Hermes does internally

1. Detects the `trendingcontent` skill from the description match
2. Loads the full SKILL.md via `skill_view("social-media/trendingcontent")`
3. Maps the request: `--days=7`, `--platform=twitter`, `--tone=viral`, `--lang=es`
4. Runs the script:

```bash
python ~/.hermes/skills/social-media/trendingcontent/scripts/trendingcontent.py \
  "inteligencia artificial" \
  --days=7 \
  --platform=twitter \
  --tone=viral \
  --lang=es \
  --quick
```

5. Reads the research summary and content brief
6. Writes the Twitter thread based on real trending data

## Example output

---

**Research highlights shared by the agent:**

> This week's top trending AI stories: GPT-5 announced with multimodal reasoning (+42k upvotes on r/MachineLearning), Mistral releases open-weights model outperforming GPT-4 on benchmarks, and a viral YouTube video explaining "why AI agents will replace search engines" reached 2M views in 3 days.

---

**Generated Twitter thread:**

```
1/ La IA está a punto de cambiar algo que usás todos los días, y casi nadie lo está viendo.

🧵 Hilo

2/ Esta semana, un video con 2M de vistas en YouTube preguntó: "¿Para qué vas a googlear si podés preguntarle a un agente?"

La respuesta está redefiniendo cómo interactuamos con internet.

3/ Mientras tanto, Mistral acaba de lanzar un modelo de código abierto que supera a GPT-4 en benchmarks clave.

El código está disponible para cualquiera. Gratis. Sin restricciones.

Esto NO pasaba hace 2 años.

4/ Y si pensabas que OpenAI dormía, GPT-5 fue anunciado esta semana con razonamiento multimodal nativo.

42.000 upvotes en r/MachineLearning en 24 horas. La comunidad explotó.

5/ El patrón que emerge es claro:
→ Los modelos open-source alcanzan a los cerrados
→ Los agentes reemplazan flujos manuales
→ La curva de adopción se acelera

Estamos en el punto de inflexión.

6/ El dato más sorprendente de la semana: el 34% de los desarrolladores encuestados ya usa IA para más del 50% de su código.

Hace 12 meses ese número era el 8%.

7/ ¿Qué significa todo esto?

Que la ventaja competitiva ya no está en saber programar. Está en saber qué pedirle a la IA.

¿Vos ya la estás usando para tu trabajo? Contame en los comentarios 👇

RT si creés que alguien necesita leer esto.
```

---

## Adjust the result

Ask the agent to refine:

```
Hacelo más corto, máximo 5 tweets, y enfocate solo en el dato del open-source.
```

```
Cambiá el tono a más profesional, que lo pueda usar en mi cuenta de empresa.
```
