function createRental(bookId) {
    $.ajax({
        method: "POST",
        url: "/rental/books-rental",
        contentType: "application/json",
        data: JSON.stringify({
            book_id: Number(bookId)
        })
    }).done(function (res) {
        alert(res.message)
        window.location.reload();
    }).fail(function (res) {
        alert(res.responseJSON.message)
    });
}