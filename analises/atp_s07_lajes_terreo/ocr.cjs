const {createWorker}=require('C:/Users/joao.severgnini/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/tesseract.js');
const fs=require('fs');
(async()=>{const w=await createWorker('eng');for(const n of ['7202','7214','7301','7302','7303','7304','7305','7306','7307','7308']){let r=await w.recognize(n+'_ocr.png',{}, {text:true,tsv:true});fs.writeFileSync(n+'_ocr.txt',r.data.text);fs.writeFileSync(n+'_ocr.tsv',r.data.tsv);console.log(n,r.data.text.slice(-2500));}await w.terminate();})();
