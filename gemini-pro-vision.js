import dotenv from "dotenv";
import * as fs from 'fs';
import { GoogleGenerativeAI} from '@google/generative-ai';
dotenv.config();
const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);
function fileToGenerativePart(path, mimeType){
    return {
        inlineData:{
            data:Buffer.from(fs.readFileSync(path)).toString('base64'),
            mimeType,
        },
    };
}
async function runPrompt() {
    const model = genAI.getGenerativeModel({model:"gemini-2.5-pro"});

    const prompt = "analyze the image and show insights";
    const imageParts=[fileToGenerativePart("program.jpg","image/jpeg")];
    const result = await model.generateContent([prompt,...imageParts]);
    const response = await result.response;
    const text = response.text();
    console.log(text);
}
runPrompt();