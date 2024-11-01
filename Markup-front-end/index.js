pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.12.313/pdf.worker.min.js';
var subjects = {
    "ADT302": "Big Data Analytics",
    "MCN301": "Disaster Management",
    "HUT200": "Professional Ethics",
    "MCN202": "Constitution of India",
    "MCN201": "Sustainable Engineering"
};

var isPressed=0;
let uploadElement= document.getElementById("QUploadReal");
let AnsweruploadElement= document.getElementById("AUploadReal");
let defaultQuestionText="Browse Question Paper from your computer";
let oldQuestionText="";
let defaultAnswerText="Browse Answer Sheets from your computer";
let oldAnswerText="";
let jsonArray;
var Questions;
var table_content='';
var tfootContent='';
var preloader='<svg role="img" aria-label="Mouth and eyes come from 9:00 and rotate clockwise into position, right eye blinks, then all parts rotate and merge into 3:00" class="smiley" viewBox="0 0 128 128" width="128px" height="128px"><defs><clipPath id="smiley-eyes"><circle class="smiley__eye1" cx="64" cy="64" r="8" transform="rotate(-40,64,64) translate(0,-56)" /><circle class="smiley__eye2" cx="64" cy="64" r="8" transform="rotate(40,64,64) translate(0,-56)" /></clipPath><linearGradient id="smiley-grad" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#000" /><stop offset="100%" stop-color="#fff" /></linearGradient><mask id="smiley-mask"><rect x="0" y="0" width="128" height="128" fill="url(#smiley-grad)" /></mask></defs><g stroke-linecap="round" stroke-width="12" stroke-dasharray="175.93 351.86"><g><rect fill="hsl(193,90%,50%)" width="128" height="64" clip-path="url(#smiley-eyes)" /><g fill="none" stroke="hsl(193,90%,50%)"><circle class="smiley__mouth1" cx="64" cy="64" r="56" transform="rotate(180,64,64)" /><circle class="smiley__mouth2" cx="64" cy="64" r="56" transform="rotate(0,64,64)" /></g></g><g mask="url(#smiley-mask)"><rect fill="hsl(223,90%,50%)" width="128" height="64" clip-path="url(#smiley-eyes)" /><g fill="none" stroke="hsl(223,90%,50%)"><circle class="smiley__mouth1" cx="64" cy="64" r="56" transform="rotate(180,64,64)" /><circle class="smiley__mouth2" cx="64" cy="64" r="56" transform="rotate(0,64,64)" /></g></g></g></svg>';
document.getElementById("QUploadText").innerHTML=defaultQuestionText;

function Markup_start(){
    if (isPressed==1){
        alert("No Can Do!");
    }
    else{
        document.getElementById("MarkupInitally").style.display="none";
        document.getElementById("MarkupInstructions").style.display="flex";
        isPressed=1;
    }
}

function Markup_Instr(){
    document.getElementById("MarkupInstructions").style.display="none";
    document.getElementById("MarkupQuestionUpload").style.display="flex";
    document.getElementById("QUploadChanger").setAttribute("onclick", "QuestionUpload()");
}

function homeBtn(){
    
    window.location.replace("index.html");
}
function aboutBtn(){
    window.location.replace("about.html");
}

function QuestionUpload(){
    uploadElement.click();
}
uploadElement.addEventListener("change", function(){
    if (uploadElement.files.length > 0 && uploadElement.files.item(0) !== null) {
        newQuestionText = uploadElement.files.item(0).name;
        document.getElementById("QUploadText").innerHTML=newQuestionText;
        oldQuestionText=newQuestionText;
    }
    else{
        document.getElementById("QUploadText").innerHTML=defaultQuestionText;
    }
    
});

document.getElementById("QUploadBtn").addEventListener("click",function(){
    const QuestionFile=uploadElement.files[0];
    if(!QuestionFile){
        alert("No file selected.");
    }
    else{
        const reader = new FileReader();
        reader.onload = function() {
            const typedArray = new Uint8Array(this.result);
            
            loadPdf(QuestionFile,typedArray);
        };
        reader.readAsArrayBuffer(QuestionFile);
    }
})
let temp_s=1;
function loadPdf(QuestionFile,data) {
    pdfjsLib.getDocument(data).promise.then(function(pdf) {
        const totalPages = pdf.numPages;
        let allText = '';

        // Extract text from 1st page
        pdf.getPage(1).then(function(page) {
            page.getTextContent().then(function(textContent) {
                textContent.items.forEach(function(textItem) {
                    allText += textItem.str + '\n'; 
                });
                
                const subjectCodeRegex = /ADT\s*302/g; 
                const matches = allText.match(subjectCodeRegex);
                if (matches && matches.length > 0) {
                    const firstMatch = matches[0];
                    console.log("First Subject Code found: ", firstMatch);
                    // Perform actions for the first match here
                    const subjectName = subjects[firstMatch.trim()];
                    if (subjectName) {
                        document.getElementById("QUploadText").innerHTML='<div class="Qpre"><div class="loader"></div>Loading Please Wait</div>';
                        document.getElementById("QUploadChanger").setAttribute("onclick", "")
                        document.getElementById("QUploadBtn").style.display="none";
                        console.log("Subject Name: ", subjectName, "\nSubject Code: ", firstMatch.trim());
                        const formData = new FormData();
                        formData.append('file', QuestionFile);
                        fetch('http://127.0.0.1:5000/process-pdf', {
                            method: 'POST',
                            body: formData
                        })
                        .then(response => response.json())
                        .then(data => {
                            //console.log('Response from server:', data);
                            if (data && data.Message === "PDF processed successfully") {
                                Questions = JSON.parse(data.Data);
                                //console.log('Questions:', Questions[0]['Questions']);
                                console.log('Questions:', Questions);
                                jsonArray = JSON.parse(data.Data);
                                QFinished(subjectName);
                            }
                            else{
                                alert(data.Message);
                                document.getElementById("QUploadText").innerHTML=oldQuestionText;
                                document.getElementById("QUploadBtn").style.display="flex";
                                document.getElementById("QUploadChanger").setAttribute("onclick", "QuestionUpload()");
                            }
                        })
                        .catch(error => {
                            alert("Error"+error);
                            document.getElementById("QUploadText").innerHTML=oldQuestionText;
                            document.getElementById("QUploadBtn").style.display="flex";
                            document.getElementById("QUploadChanger").setAttribute("onclick", "QuestionUpload()");
                        });
                    }
                } else {
                    alert("The Question paper should follow a proper structure!");
                }
            });
        });
    }).catch(function(error) {
        console.error('Error loading PDF:', error);
    });
}
function AnswerUpload(){
    AnsweruploadElement.click();
}
function QFinished(subjectName){
    document.getElementById("MarkupQuestionUpload").style.display="none";
    document.getElementById("MarkupAnswerUpload").style.display="flex";
    document.getElementById("AUploadSubject").innerHTML="SUBJECT: "+subjectName;
    document.getElementById("AUploadTQ").innerHTML="Total Question: "+jsonArray.length;
    document.getElementById("AUploadChanger").setAttribute("onclick", "AnswerUpload()");
    document.getElementById("AUploadText").innerHTML=defaultAnswerText;
}

AnsweruploadElement.addEventListener("change", function(){
    if (AnsweruploadElement.files.length > 0 && AnsweruploadElement.files.item(0) !== null) {
        newAnswerText = AnsweruploadElement.files.item(0).name;
        document.getElementById("AUploadText").innerHTML=newAnswerText;
        oldAnswerText=newAnswerText;
    }
    else{
        document.getElementById("AUploadText").innerHTML=defaultAnswerText;
    }
    
});

document.getElementById("AUploadBtn").addEventListener("click",function(){
    const AnswerFile=AnsweruploadElement.files[0];
    if(!AnswerFile){
        alert("No file selected.");
    }
    else{
        loadAnswerPdf(AnswerFile);
    }
})

function loadAnswerPdf(AnswerFile) {
    document.getElementById("AUploadText").innerHTML="Loading Please Wait!&nbsp"+preloader;
    document.getElementById("AUploadChanger").setAttribute("onclick", "")
    document.getElementById("AUploadBtn").style.display="none";
    const formData = new FormData();
    formData.append('file', AnswerFile);
    fetch('http://127.0.0.1:5000/process-answer', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        //console.log('Response from server:', data);
        //jsonArray = JSON.parse(data.Data);
        if (data && data.Message === "Answer processed successfully") {
            var Answers = JSON.parse(data.Answer);
            var Marks = JSON.parse(data.Mark);
            AnswerProcessed(data.Answer,Marks,data.FD,data.SD);
        }
        else{
            alert(data.Message);
            document.getElementById("AUploadText").innerHTML=oldAnswerText;
            document.getElementById("AUploadBtn").style.display="flex";
            document.getElementById("AUploadChanger").setAttribute("onclick", "AnswerUpload()");
        }
    })
    .catch(error => {
        alert("Error"+error);
        document.getElementById("AUploadText").innerHTML=oldAnswerText;
        document.getElementById("AUploadBtn").style.display="flex";
        document.getElementById("AUploadChanger").setAttribute("onclick", "AnswerUpload()");
    });
}

function AnswerProcessed(Answers,Marks,FD,SD){
    var keys=Object.keys(Marks);
    var value;
    var sum=0;
    var Qarray=[]
    var FR=[]
    j=0;
    for (var i = 0; i < Questions.length; i++) {
        Qarray.push(Questions[i]['Questions']);
        FR.push(Questions[i]['Requirement']);
        var key = keys[j];
        if(parseInt(key)===(i+1)){
            value = Marks[key];
            sum=sum+parseInt(value);
            j=j+1;
        }else{
            value = '0';
        }
        table_content=table_content+'<tr><td>'+(i+1).toString()+'</td><td>'+value+'</td><td>'+Questions[i]['Mark']+'</td></tr>';
    }
    tfootContent='<tr><th>Total</th><th>'+sum.toString()+'</th><th>50</th></tr>';
    localStorage.setItem('tableContent', table_content);
    localStorage.setItem('tfootContent', tfootContent);
    localStorage.setItem('Answers', Answers);
    localStorage.setItem('FD', FD);
    localStorage.setItem('SD', SD);
    localStorage.setItem('Questions', Qarray);
    localStorage.setItem('FR', FR);


    // Redirect to test.html with query parameters
    window.location.href = "result.html";
    //document.getElementById("MarkupResultBody").innerHTML=table_content;
}