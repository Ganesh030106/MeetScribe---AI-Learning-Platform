import dotenv from "dotenv";
import { GoogleGenerativeAI} from '@google/generative-ai';
import express from "express";
dotenv.config();
const app = express();
import * as fs from 'fs';

function fileToGenerativePart(path, mimeType){
    return {
        inlineData:{
            data:Buffer.from(fs.readFileSync(path)).toString('base64'),
            mimeType,
        },
    };
}
app.use(express.static("public"));
app.get("/",async (req,res)=>{
    const model = genAI.getGenerativeModel({model:"gemini-2.5-pro"});

    const prompt = "Write a short poem about the sea with rhyme.";
    const result = await model.generateContent(prompt);
    const response = await result.response;
    const text = response.text();
    console.log(text);
    
    res.render("index.ejs",{data:text});

})
app.get("/image",async (req,res)=>{
    const model = genAI.getGenerativeModel({model:"gemini-2.5-pro"});

    const prompt = "give me the code in this file";
    const imageParts=[fileToGenerativePart("stream.jpg","image/jpeg")];
    const result = await model.generateContent([prompt,...imageParts]);
    const response = await result.response;
    const text = response.text();
    console.log(text);
    res.render("image.ejs",{data:text});

})
const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);
async function runPrompt() {
    const model = genAI.getGenerativeModel({model:"gemini-2.5-pro"});

    const prompt = "Write a short poem about the sea with rhyme.";
    const result = await model.generateContent(prompt);
    const response = await result.response;
    const text = response.text();
    console.log(text);
    return text;
}
runPrompt();
app.listen(5000, () =>
  console.log("🚀 Server running at http://localhost:5000")
);