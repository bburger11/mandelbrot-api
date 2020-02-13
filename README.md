# mandelbrot-api

C program and python API to retrieve bitmap images generated from the Mandelbrot set.

This API was built for my Mandelbrot web application. The API has two methods:

Post
----
`POST <base_url>/bitmap/s_val/x_val/y_val/` -- creates image at `(x_val, y_val)` with scale value `v_val`.
    
It returns the name of the file created, which is determined by a simple md5 checksum on the string:
    
`s:{s}x:{x}y:{y}`
    
Example: 
POST `<base_url>/bitmap/2/0/0`
        
Returns: `{"result": "success", "filename": "b69e2b00ac625357d8de1b3297902133.bmp"}`
    
Get
---    
`GET <base_url>/bitmap/filename/` -- retrieves the raw bytes of image specified by filename.

Example: 
GET `<base_url>/bitmap/b69e2b00ac625357d8de1b3297902133.bmp/`

Returns: The Image in raw bytes data
