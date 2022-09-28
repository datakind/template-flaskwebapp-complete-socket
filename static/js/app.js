// Drag and drop code that is use to allow drag and drop
    let dropArea = document.querySelector('.droparea');
    ;['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, preventDefaults, false)
    })

    function preventDefaults(e) {
        e.preventDefault()
        e.stopPropagation()
    }

    const highlight = () => dropArea.classList.add("green-border");
    const unhighlight = () => dropArea.classList.remove("green-border");

    ;['dragenter', 'dragover'].forEach(eventName => {
        dropArea.addEventListener(eventName, highlight, false)
    })

    ;['dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, unhighlight, false)
    })

    dropArea.addEventListener("drop", handleDrop, false);

    function handleDrop(e) {
        let dt = e.dataTransfer
        let files = dt.files
        handleFiles(files);
    }

    // A function that handles the uploading of the file
    function handleFiles(files) {
        loadtimegui = document.getElementById("loadtime")
        loadtimetext = document.createElement('p')
        loadtimetext.innerHTML = "Uploading file... (Please wait 10-20 seconds)"
        loadtimetext.style.cssText += 'float: left;'
        loadicon = document.createElement("div")
        loadicon.classList.add("dots-bars-4")
        loadicon.setAttribute("id","loadiconid")
        loadicon.style.cssText += 'margin-left: auto;margin-right: auto;'
        loadtimegui.appendChild(loadtimetext)
        loadtimegui.appendChild(loadicon);
        {
        ([...files]).forEach(uploadFile)}
    }
    async function uploadFile(file) {
        const url = '/'
        let formData = new FormData()
        console.log(file);
        formData.append("file", file);

        let responseOptions = {
            method: 'POST',
            files: file,
            body: formData
        }
        console.log(responseOptions);

        await fetch(url, responseOptions)
            .then(() => { console.log('Finished'); })
            .catch(() => { /* Error. Inform the user */ })
    }


    // Websocket initialization
    var socket = io();

    // runTool websocket code
    $('#runTool').click(function(event) {
                socket.emit('runTool');
                loadtimegui = document.getElementById("loadtime")
                loadtimetext = document.createElement('p')
                loadtimetext.innerHTML = "STARTING TERMINAL LOGGER........"
                loadtimetext.style.cssText += 'float: left;'
                loadicon = document.createElement("div")
                loadicon.classList.add("dots-bars-4")
                loadicon.setAttribute("id","loadiconid")
                loadicon.style.cssText += 'margin-left: auto;margin-right: auto;'
                loadtimegui.appendChild(loadtimetext)
                loadtimegui.appendChild(loadicon)
                return false;
            })


    // A websocket for different error catches
    socket.on('logerror', function(msg){
        if (String(msg.errormessage) == "File Missing"){
            document.getElementById("loadtime").innerHTML = ""
            document.getElementById("output").innerHTML = ""
            $('#output').append(msg.loginfo)
        } else {
            $('#output').append(msg.loginfo)
        }
    })

    // A websocket to clear output of the logger on screen
    socket.on('clearoutput', function(msg) {
        document.getElementById("output").innerHTML = ""
    })

    // The websocket that pipes the runtime interpreter to the screen
    socket.on('logTool', function(msg) {
        console.log('logTool')
        console.log(msg.loginfo)
        $('#output').append(msg.loginfo)
        }
    )

    // A websocket to let the user know the upload is completed
    socket.on('uploadcomplete', function(msg) {
        console.log('upload is complete')
        document.getElementById("loadtime").innerHTML = "" 
        loadtimetext = document.createElement('p')
        loadtimetext.innerHTML = "Upload completed"
        loadtimetext.style.cssText += 'float: left;'
        loadtimegui.appendChild(loadtimetext)

    })

    // A websocket to let the user know the upload is completed
    socket.on('runToolComplete', function(msg) {
        loadtimeid = document.getElementById("loadtime")
        loadtimeid.innerHTML = "OUTPUT COMPLETED! RESULTS BELOW: "

    })