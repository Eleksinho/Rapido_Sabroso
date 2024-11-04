// ---------Responsive-navbar-active-animation-----------
function test() {
  var tabsNewAnim = $("#navbarSupportedContent");
  var activeItemNewAnim = tabsNewAnim.find(".active");

  if (activeItemNewAnim.length > 0) {
    var activeWidthNewAnimHeight = activeItemNewAnim.innerHeight();
    var activeWidthNewAnimWidth = activeItemNewAnim.innerWidth();
    var itemPosNewAnimTop = activeItemNewAnim.position();
    var itemPosNewAnimLeft = activeItemNewAnim.position();
    
    $(".hori-selector").css({
      top: itemPosNewAnimTop.top + "px",
      left: itemPosNewAnimLeft.left + "px",
      height: activeWidthNewAnimHeight + "px",
      width: activeWidthNewAnimWidth + "px"
    });
  }
}

$(document).ready(function () {
  test(); // Ejecuta test() inmediatamente

  $("#navbarSupportedContent").on("click", "li", function () {
    $("#navbarSupportedContent ul li").removeClass("active");
    $(this).addClass("active");
    test(); // Actualiza el selector después de un clic
  });

  $(".navbar-toggler").click(function () {
    $(".navbar-collapse").slideToggle(300);
    setTimeout(test, 300); // Asegúrate de que el selector se actualice después del toggle
  });

  // Establece la clase activa en el enlace correspondiente al cargar la página
  var path = window.location.pathname.split("/").pop() || "index.html";
  $('#navbarSupportedContent ul li a[href="' + path + '"]').parent().addClass("active");
});

// Recalcula la posición y tamaño del selector en el redimensionamiento
$(window).on("resize", function () {
  setTimeout(test, 500);
});
