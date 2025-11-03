import { GoogleGenerativeAI } from "@google/generative-ai";
import dotenv from "dotenv";
import fs from "fs";

dotenv.config();

async function generateImage() {
  try {
    // Initialize Gemini client
    const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);

    // Use an image-capable model
    const model = genAI.getGenerativeModel({
      model: "models/gemini-2.5-flash-image",
    });

    // 🔥 Your image prompt here
    const prompt = "A serene Japanese garden with cherry blossoms and a small bridge";

    console.log("🧠 Generating image for prompt:", prompt);

    // Generate image
    const result = await model.generateContent([
      {
        role: "user",
        parts: [{ text: prompt }],
      },
    ]);

    // Extract base64 image data
    const imageBase64 = result.response.candidates[0].content.parts[0].inlineData.data;

    // Save image to file
    const imageBuffer = Buffer.from(imageBase64, "base64");
    fs.writeFileSync("generated_image.png", imageBuffer);

    console.log("✅ Image generated successfully! Saved as generated_image.png");
  } catch (err) {
    console.error("❌ Error generating image:", err);
  }
}

generateImage();
