const lanIP = `${window.location.hostname}:5000`;
const socket = io(`http://${lanIP}`);

const provider = 'https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png';
const copyright = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Tiles style by <a href="https://www.hotosm.org/" target="_blank">Humanitarian OpenStreetMap Team</a> hosted by <a href="https://openstreetmap.fr/" target="_blank">OpenStreetMap France</a>';
let map, layergroup

let idpositie, idboek, htmlBook, htmlInfo, htmlAanpassen, htmlVoorige, htmlLibraries;

const maakMarker = function(long , lat, adres, bibnaam){
  // console.log(coord);
  const arr_coord = []
  arr_coord.push(long); 
  arr_coord.push(lat); 
  layergroup.clearLayers();
  let marker = L.marker(arr_coord).addTo(layergroup);
  marker.bindPopup(`<h3>${bibnaam}</h3><em>${adres}</em>`);
};

const addEventToLibrary = function() {
  const libraries = document.querySelectorAll(".js-bib");
  for (const library of libraries){
    library.addEventListener('click', function(){
      const long = this.getAttribute("long");
      const lat = this.getAttribute("lat");
      const adres = this.getAttribute("adres");
      const bibnaam = this.innerHTML;
      maakMarker(long, lat, adres, bibnaam);
      // console.log(long)
    });
  }
}

const toggleNav = function() {
  let toggleTrigger = document.querySelectorAll(".js-toggle-nav");
  for (let i = 0; i < toggleTrigger.length; i++) {
      toggleTrigger[i].addEventListener("click", function() {
          document.querySelector("body").classList.toggle("has-mobile-nav");
      })
  }
}

const listenToClickBook = function(){
    const boeken = document.querySelectorAll(".js-book");
    for (const boek of boeken){
        boek.addEventListener("click", function () {
            idboek = boek.getAttribute('id-boek');
            console.log(idboek)
            socket.emit("F2B_idboek", idboek)
            window.location.href=`info.html`
        });
    };
};

const shutdown = function(){
    const shutdown = document.querySelector(".js-shutdown")
    shutdown.addEventListener("click", function () {
      socket.emit("F2B_sutddown",);
    });
};

const aanpassenBoek = function(){
  const iconAanpassen = document.querySelector(".js-icon-aanpassen")
  console.log("icon gevonden")
  console.log(iconAanpassen)
  iconAanpassen.addEventListener("click", function () {
    console.log("click")
    window.location.href=`aanpassen.html`
  });
  // let iconAanpassen = document.querySelectorAll(".js-icon-aanpassen");
  // for (let i = 0; i < iconAanpassen.length; i++) {
  //         iconAanpassen[i].addEventListener("click", function() {
  //           window.location.href=`aanpassen.html`
  //     })
  // }
};

const verleng = function(){
  const vastePeriode = document.querySelector(".js-4-weeken")
  const selectedDate = document.querySelector(".js-selected-date")
  // console.log("icon gevonden")
  // console.log(iconAanpassen)
  vastePeriode.addEventListener("click", function () {
    // console.log("click")
    socket.emit("F2B_verleng_4",)
    socket.emit("F2B_idboek", 0)
    window.location.href=`index.html`

  });

  selectedDate.addEventListener("click", function () {
    const date = document.getElementById("extendBook").value
    // console.log("click")
    socket.emit("F2B_verleng",date)
    socket.emit("F2B_idboek", 0)
    // console.log(date)
    window.location.href=`index.html`

  });
  
};

const listenToUI = function(){
  
  shutdown();

  const addBook = document.querySelector(".js-add-book")
  if (addBook){
    
    addBook.addEventListener("click", function () {
      window.location.href=`aanpassen.html`
    });
  
  };

  toggleNav();
  if (htmlInfo){
    aanpassenBoek();
    verleng();

    const handIn = document.querySelector(".js-hand-in")
    handIn.addEventListener("click", function () {
      console.log("click")
      socket.emit("F2B_indiennen",)
      // console.log(date)
      socket.emit("F2B_idboek", 0)
      window.location.href=`index.html`
  
    });
  };

  if (htmlAanpassen){
    const adjust = document.querySelector(".js-adjust")
    adjust.addEventListener("click", function () {
        
      // console.log("click")
      const json = {
        name: document.querySelector(".js-boek").value,
        author: document.querySelector(".js-author").value,
        library: document.querySelector(".js-library").value,
        indiennen: document.querySelector(".js-datum").value
      };
      console.log(json)

      socket.emit("F2B_aanpassen",json)
      // console.log(date)
      window.location.href=`index.html`

    });
  };

  if (htmlLibraries){
    layergroup = L.layerGroup().addTo(map);
    addEventToLibrary();
  };
 

};


const listenToSocket = function() {
  // console.log("check")

  socket.on("connected", function () {
      console.log("verbonden met socket webserver");
  });

  if (htmlBook) {
    socket.emit("F2B_check_nieuw_book",)

    socket.on("B2F_status_positions", function (jsonObject) {
        // console.log("iets verzonden");
        // console.log(jsonObject);
        
        let htmlString =`<h2>Current books:</h2>`;
        for (let book of jsonObject.positions) {
            htmlString += `<article id-boek="${book.idboek}" class="o-layout o-layout--align-center c-border js-book u-mb-lg">
            <div class="o-layout__item u-1-of-6">
                <h2 class="o-layout o-layout--justify-center o-cijfer u-mb-clear">
                  ${book.idpositie}
                </h2>
            </div>  
            <div class="o-layout__item u-4-of-5 c-border__info u-p-sm">
                <h3>
                ${book.naam}
                </h3>
                <div class="o-layout o-layout--align-center ">
                    <div class="o-layout__item u-1-of-2">
                      <p>
                        Return date:
                      </p>
                    </div>
                    <div class="o-layout__item u-1-of-2">
                      <p>
                      ${book.inleverdatum}
                      </p>
                    </div>
                </div>
                <div class="o-layout o-layout--align-center">
                  <div class="o-layout__item u-1-of-2">
                    <p>
                      Library:
                    </p>
                  </div>
                  <div class="o-layout__item u-1-of-2">
                    <p>
                    ${book.naambib}
                    </p>
                  </div>
              </div>
            </div>
          </article>`;
        };
        
        htmlBook.innerHTML = htmlString;

        listenToClickBook();
    });

    socket.on("B2F_check_book", function (jsonObject) {
        console.log("iets verzonden");
        console.log(jsonObject);
        document.querySelector(".js-nieuw-book").classList.remove("c-deteted");
        document.querySelector(".js-position").innerHTML = jsonObject.positie;
        // console.log(jsonObject.positie)
        // 

        
        // htmlBook.innerHTML = htmlString;

        // listenToClickBook();
    });
  };

  if (htmlInfo){
    socket.emit("F2B_infoboek",)
    socket.on("B2F_info_boek", function (jsonObject){
      console.log(jsonObject)
      let htmlString =`
      <div id-position='${jsonObject.boek.idpositie}' class="o-layout u-mb-md">
        <p class="o-layout__item u-1-of-2 u-1-of-3-bp1">Position: </p>
        <p class="o-layout__item u-1-of-2 u-2-of-3-bp1">${jsonObject.boek.idpositie}</p>
      </div>  
      <div id-book='${jsonObject.boek.idboek}' class="o-layout u-mb-md">
        <p class="o-layout__item u-1-of-2 u-1-of-3-bp1">Name:</p>
        <p class="o-layout__item u-1-of-2 u-2-of-3-bp1">${jsonObject.boek.naam}</p>
      </div>
      <div class="o-layout u-mb-md">
        <p class="o-layout__item u-1-of-2 u-1-of-3-bp1">Author</p>
        <p class="o-layout__item u-1-of-2 u-2-of-3-bp1">${jsonObject.boek.author}</p>
      </div>
      <div id-bib='${jsonObject.boek.idbibliotheek}' class="o-layout u-mb-md">
        <p class="o-layout__item u-1-of-2 u-1-of-3-bp1">Library:</p>
        <p class="o-layout__item u-1-of-2 u-2-of-3-bp1">${jsonObject.boek.naambib}</p>
      </div>
      <div class="o-layout u-mb-xxl">
        <p class="o-layout__item u-1-of-2 u-1-of-3-bp1">Return Date:</p>
        <p class="o-layout__item u-1-of-2 u-2-of-3-bp1">${jsonObject.boek.inleverdatum}</p>
      </div>`;
        
        htmlInfo.innerHTML = htmlString;
      
    });
  };


  if (htmlAanpassen){
    socket.emit("F2B_Aanpassenboek",)
    
    socket.on("B2F_Librarys", function (jsonObject){
      htmlLibrary = document.querySelector(".js-library");
      // console.log(jsonObject)
      let htmlString =`<option value="" disabled selected>Choose a library</option>`;
      for (const library of jsonObject.librarys){
        htmlString += `<option id="${library.idbibliotheek}" value="${library.naam}">${library.naam}</option>`

      };
      // console.log(htmlString)
      htmlLibrary.innerHTML = htmlString
    });


    socket.on("B2F_Aanpassen_boek", function (jsonObject){
      console.log(jsonObject)
      document.getElementById("NameBook").value = jsonObject.boek.naam;
      document.getElementById("Author").value = jsonObject.boek.author;
      document.getElementById("extendBook").value = jsonObject.boek.inleverdatum;
      document.getElementById(`${jsonObject.boek.idbibliotheek}`).selected = 'selected';
    
      // htmlNaam.Value = jsonObject.boek.naam
      // console.log(jsonObject.boek.naam)
    });
  };
  
  if (htmlVoorige) {
    socket.emit("F2B_previous_books",)

    socket.on("B2F_previous_books", function (jsonObject) {
        // console.log("iets verzonden");
        // console.log(jsonObject);
        
        let htmlString =``;
        for (let book of jsonObject.books) {
            htmlString += `<article id-boek="${book.idboek}" class="o-layout__item u-1-of-2-bp3 u-mb-md ">
            <div class="o-layout o-layout--align-center c-border u-mrl-md ">
                <div class="u-p-sm o-layout o-layout--align-center"> 
                    <h3 class="o-layout__item">
                      ${book.naam}
                    </h3>
                    <div class="o-layout__item o-layout o-layout--align-center">
                        <div class="o-layout__item u-1-of-2">
                            <p>
                            Library:
                            </p>
                        </div>
                        <div class="o-layout__item u-1-of-2">
                            <p>
                            ${book.naambib}
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </article>`;
        };
        
        htmlVoorige.innerHTML = htmlString;

        listenToClickBook();
    });

  };

  if (htmlLibraries){
    socket.emit("F2B_libraries",)

    socket.on("B2F_libraries", function (jsonObject) {
      const htmlBib = document.querySelector(".js-bibs")
      // console.log("iets verzonden");
      // console.log(jsonObject);
      
      let htmlString =``;
      for (let library of jsonObject.libraries) {
          htmlString += `<div class="o-layout__item u-1-of-4-bp3 u-1-of-2-bp1">
          <div long="${library.long}" lat="${library.lat}" adres="${library.locatie}" class="c-border u-p-sm u-mb-lg u-mrl-sm o-layout o-layout--justify-center js-bib">
            ${library.naam}
          </div>
        </div>`;
      };
      
      htmlBib.innerHTML = htmlString;
      addEventToLibrary();
      // listenToClickBook();
  });
    

  }

};


document.addEventListener("DOMContentLoaded", function () {
    console.info("DOM geladen");
    htmlBook = document.querySelector(".js-books");
    htmlInfo = document.querySelector(".js-info");
    htmlAanpassen = document.querySelector(".js-aanpassen");
    htmlVoorige = document.querySelector(".js-vorige-boeken");
    htmlLibraries = document.querySelector(".js-libraries");
    
    

    if (htmlLibraries){
      map = L.map("mapid").setView([51.041028, 3.398512], 9);
      L.tileLayer(provider, {attribution: copyright}).addTo(map);
    }

    listenToUI();
    listenToSocket();

  });