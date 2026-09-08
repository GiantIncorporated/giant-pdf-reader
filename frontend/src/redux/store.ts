import {configureStore} from "@reduxjs/toolkit";
import pdfReducer from "../features/reader/pdfSlice"

export default configureStore({
    reducer: {
        pdf: pdfReducer
    }
})
