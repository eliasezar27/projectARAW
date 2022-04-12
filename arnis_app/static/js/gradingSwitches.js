$(document).ready(function(){

    let checkInterval = true;
    let interval = setInterval(function(){
        if ($("#video-feed").height() != 0){
            $('#video-feed-loader').addClass("d-none");
            clearInterval(interval);
        }

    }, 100);

    console.log('pasok');
    var grading = 0;
    var classification = 0;

    if($('h1').text().toLowerCase() == 'grading') {
        grading = 1;
        classification = 0;
    }else{
        grading = 0;
        classification = 1;
    }

    var skeletonOption = 0;
    var angleOption = 0;
    var fpsOption = 0;
    var poseKey = 1;
    var gradeContainer = 0;
    var student_id = $('#saveGrade').attr('student_id');
    console.log(student_id);
     req = $.ajax({
        url : '/grading/switches',
        type : 'POST',
        data : {
                grading : grading,
                classification, classification,
                poseKey : poseKey,
                skeletonOption : skeletonOption,
                angleOption : angleOption,
                fpsOption : fpsOption,
                gradeContainer : gradeContainer,
                student_id : student_id
                }
    });

    req.done(function(data){
        console.log(data.result);
    });


    $("#showSkeletonSwitch").change(function(){
        var skeletonOption = 0;
         if($(this).is(':checked')){
            skeletonOption = 1;
         }else{
            skeletonOption = 0;
         }
        console.log(skeletonOption);
         req = $.ajax({
            url : '/grading/switches',
            type : 'POST',
            data : {
                    skeletonOption : skeletonOption
                    }
        });

        req.done(function(data){
            console.log(data.result);
        });
    });


    $("#showAngleSwitch").change(function(){
        var angleOption = 0;
         if($(this).is(':checked')){
            angleOption = 1;
         }else{
            angleOption = 0;
         }
        console.log(angleOption);
         req = $.ajax({
            url : '/grading/switches',
            type : 'POST',
            data : {
                    angleOption : angleOption
                    }
        });

        req.done(function(data){
            console.log(data.result);
        });
    });

    $("#showFPS").change(function(){
        var fpsOption = 0;
         if($(this).is(':checked')){
            fpsOption = 1;
         }else{
            fpsOption = 0;
         }
        console.log(fpsOption);
         req = $.ajax({
            url : '/grading/switches',
            type : 'POST',
            data : {
                    fpsOption : fpsOption
                    }
        });

        req.done(function(data){
            console.log(data.result);
        });
    });


 });