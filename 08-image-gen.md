# Demo 8: Image Generation

**Feature**: Agy can generate images on-the-fly using text-to-image capabilities — useful for UI mockups, assets, and creative work.

## What Can Agy Generate?

- UI mockups and wireframes
- App icons, logos, and placeholder assets
- Diagrams and visual aids
- Creative/marketing images
- Any image from a text description

## Demo: Futuristic Rocket Launch

**Prompt sent to agy:**
```
Generate an image of a futuristic rocket launching from a neon-lit launchpad at night,
with the text "AGY CLI" visible on the rocket body. Save it as rocket-launch.png.
```

**What agy did:**
1. Called `GenerateImage()` tool with the detailed prompt
2. Image generated as an artifact in the conversation
3. Copied the generated image to the workspace directory
4. Confirmed the file path and provided a preview

**Result**: `rocket-launch.png` (1.7MB) saved to workspace.

## Practical Use Cases

| Use Case | Example |
|----------|---------|
| UI Prototyping | "Generate a mockup of the login page with dark mode" |
| App Assets | "Create a 512x512 app icon for a weather app" |
| Placeholder Content | "Generate 3 placeholder hero images for the landing page" |
| Documentation | "Create a diagram showing the data flow between services" |
| Branding | "Design a logo for the project with blue and white colors" |

## Key Takeaway

Image generation is built directly into agy — no need for external tools like DALL-E or Midjourney. Just describe what you need in natural language and agy generates it inline, saving it wherever you specify.
