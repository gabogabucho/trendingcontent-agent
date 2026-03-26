# Example 02 — LinkedIn Post in Spanish (Niche Topic)

## Use case

You want a LinkedIn post about a niche topic (sourdough bread / artisan bakery) for a food business account. HackerNews and TikTok won't be useful here — disable them.

## Prompt to the agent

```
Escribime un post de LinkedIn sobre las tendencias en panadería artesanal de los últimos 15 días.
Tono profesional. En español. No uses HackerNews ni TikTok como fuentes.
```

## What Hermes does internally

Maps to:

```bash
python ~/.hermes/skills/social-media/trendingcontent/scripts/trendingcontent.py \
  "panadería artesanal" \
  --days=15 \
  --platform=linkedin \
  --tone=professional \
  --lang=es \
  --disable=hackernews,tiktok
```

## Example output

---

**Research highlights:**

> Top content from Reddit (r/Breadit, r/sourdough), YouTube, and Bluesky over the last 15 days: "Cold fermentation 72h" technique went viral on r/sourdough with 8.2k upvotes, YouTube channel "Bake with Jack" released a guide on whole-wheat hydration ratios (180k views), and Bluesky bakers community is discussing the revival of ancient grains (einkorn, emmer).

---

**Generated LinkedIn post:**

```
La panadería artesanal está viviendo un momento de redescubrimiento, y los números lo confirman.

En las últimas dos semanas, la técnica de fermentación en frío de 72 horas dominó las comunidades de panaderos en todo el mundo. No es una moda: es una respuesta a años de pan industrial sin sabor ni textura.

Tres tendencias que están marcando el camino:

La fermentación lenta vuelve al centro. Tiempos de reposo más largos = más complejidad de sabor, mejor digestibilidad y mayor vida útil. Lo que antes era "demasiado técnico" ahora es accesible.

Los granos ancestrales ganan terreno. Einkorn, emmer y espelta están apareciendo en panaderías que buscan diferenciarse. Menor rendimiento, mayor valor percibido.

La comunidad digital amplifica el oficio. Canales de YouTube con más de 180k vistas por video demuestran que hay un público hambriento de técnica y proceso real.

Para quienes estamos en el sector: el consumidor actual no solo compra pan. Compra historia, proceso y transparencia.

¿Tu panadería está comunicando eso?

#PanaderíaArtesanal #Sourdough #FoodBusiness #Tendencias #Gastronomía
```

---

## Adjust the result

```
Hacelo más corto, que entre en una sola pantalla sin hacer scroll.
```

```
Agregá una pregunta al final para generar más comentarios.
```
