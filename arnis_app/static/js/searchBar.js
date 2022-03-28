$(document).ready(function() {
     $('#searchBar1, #searchBar2').on('keyup focus', function() {
          var input = $(this).val();
          var filter = input.toLowerCase();
          var selectSearch = $("#selectSearch").val();
          var selectSearch2 = $("#selectSearch2").val();

          console.log(selectSearch);

          var card1 = $('#teacherList .col-md-6');
          var card2 = $('#sectionList .col-md-6');

           let card;
           let otherCard;
          switch(selectSearch) {
            case '0':
                card1.css('display', 'block');
                card2.css('display', 'block');
                $('#chartContainer').parent().css('display', 'block');
                break;
              case '1':
                card = card1;
                otherCard = card2;
                otherCard.css('display', 'block');
                break;
              case '2':
                card = card2;
                otherCard = card1;
                otherCard.css('display', 'block');
                break;
            }

            switch(selectSearch2) {
            case '0':
                card1.css('display', 'block');
                card2.css('display', 'block');
                $('#chartContainer').parent().css('display', 'block');
                break;
              case '1':
                card = card1;
                otherCard = card2;
                otherCard.css('display', 'block');
                $('#chartContainer').parent().css('display', 'block');
                break;
              case '2':
                card = card2;
                otherCard = card1;
                otherCard.css('display', 'block');
                $('#chartContainer').parent().css('display', 'block');
                break;
            }

//          For teacher's list
            if(selectSearch == '1' || selectSearch == '2' || selectSearch2 == '1' || selectSearch2 == '2'){
              for (i = 0; i < card.length; i++) {
                if (card[i].innerText.toLowerCase().includes(filter)) {
                  card[i].style.display = "block";
                } else {
                  card[i].style.display = "none";
                  otherCard.css('display', 'none');
                  $('#chartContainer').parent().css('display', 'none')
                }
              }
            }
    });

});