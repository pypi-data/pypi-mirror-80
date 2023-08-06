/*
 * Python bindings module for libevt (pyevt)
 *
 * Copyright (C) 2011-2020, Joachim Metz <joachim.metz@gmail.com>
 *
 * Refer to AUTHORS for acknowledgements.
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Lesser General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public License
 * along with this program.  If not, see <https://www.gnu.org/licenses/>.
 */

#include <common.h>
#include <narrow_string.h>
#include <types.h>

#if defined( HAVE_STDLIB_H ) || defined( HAVE_WINAPI )
#include <stdlib.h>
#endif

#include "pyevt.h"
#include "pyevt_error.h"
#include "pyevt_event_types.h"
#include "pyevt_file.h"
#include "pyevt_file_flags.h"
#include "pyevt_file_object_io_handle.h"
#include "pyevt_libbfio.h"
#include "pyevt_libcerror.h"
#include "pyevt_libevt.h"
#include "pyevt_python.h"
#include "pyevt_record.h"
#include "pyevt_records.h"
#include "pyevt_strings.h"
#include "pyevt_unused.h"

#if !defined( LIBEVT_HAVE_BFIO )

LIBEVT_EXTERN \
int libevt_check_file_signature_file_io_handle(
     libbfio_handle_t *file_io_handle,
     libevt_error_t **error );

#endif /* !defined( LIBEVT_HAVE_BFIO ) */

/* The pyevt module methods
 */
PyMethodDef pyevt_module_methods[] = {
	{ "get_version",
	  (PyCFunction) pyevt_get_version,
	  METH_NOARGS,
	  "get_version() -> String\n"
	  "\n"
	  "Retrieves the version." },

	{ "check_file_signature",
	  (PyCFunction) pyevt_check_file_signature,
	  METH_VARARGS | METH_KEYWORDS,
	  "check_file_signature(filename) -> Boolean\n"
	  "\n"
	  "Checks if a file has a Windows Event Log (EVT) file signature." },

	{ "check_file_signature_file_object",
	  (PyCFunction) pyevt_check_file_signature_file_object,
	  METH_VARARGS | METH_KEYWORDS,
	  "check_file_signature_file_object(file_object) -> Boolean\n"
	  "\n"
	  "Checks if a file has a Windows Event Log (EVT) file signature using a file-like object." },

	{ "open",
	  (PyCFunction) pyevt_open_new_file,
	  METH_VARARGS | METH_KEYWORDS,
	  "open(filename, mode='r') -> Object\n"
	  "\n"
	  "Opens a file." },

	{ "open_file_object",
	  (PyCFunction) pyevt_open_new_file_with_file_object,
	  METH_VARARGS | METH_KEYWORDS,
	  "open_file_object(file_object, mode='r') -> Object\n"
	  "\n"
	  "Opens a file using a file-like object." },

	/* Sentinel */
	{ NULL, NULL, 0, NULL }
};

/* Retrieves the pyevt/libevt version
 * Returns a Python object if successful or NULL on error
 */
PyObject *pyevt_get_version(
           PyObject *self PYEVT_ATTRIBUTE_UNUSED,
           PyObject *arguments PYEVT_ATTRIBUTE_UNUSED )
{
	const char *errors           = NULL;
	const char *version_string   = NULL;
	size_t version_string_length = 0;

	PYEVT_UNREFERENCED_PARAMETER( self )
	PYEVT_UNREFERENCED_PARAMETER( arguments )

	Py_BEGIN_ALLOW_THREADS

	version_string = libevt_get_version();

	Py_END_ALLOW_THREADS

	version_string_length = narrow_string_length(
	                         version_string );

	/* Pass the string length to PyUnicode_DecodeUTF8
	 * otherwise it makes the end of string character is part
	 * of the string
	 */
	return( PyUnicode_DecodeUTF8(
	         version_string,
	         (Py_ssize_t) version_string_length,
	         errors ) );
}

/* Checks if a file has a Windows Event Log (EVT) file signature
 * Returns a Python object if successful or NULL on error
 */
PyObject *pyevt_check_file_signature(
           PyObject *self PYEVT_ATTRIBUTE_UNUSED,
           PyObject *arguments,
           PyObject *keywords )
{
	PyObject *string_object      = NULL;
	libcerror_error_t *error     = NULL;
	static char *function        = "pyevt_check_file_signature";
	static char *keyword_list[]  = { "filename", NULL };
	const char *filename_narrow  = NULL;
	int result                   = 0;

#if defined( HAVE_WIDE_SYSTEM_CHARACTER )
	const wchar_t *filename_wide = NULL;
#else
	PyObject *utf8_string_object = NULL;
#endif

	PYEVT_UNREFERENCED_PARAMETER( self )

	/* Note that PyArg_ParseTupleAndKeywords with "s" will force Unicode strings to be converted to narrow character string.
	 * On Windows the narrow character strings contains an extended ASCII string with a codepage. Hence we get a conversion
	 * exception. This will also fail if the default encoding is not set correctly. We cannot use "u" here either since that
	 * does not allow us to pass non Unicode string objects and Python (at least 2.7) does not seems to automatically upcast them.
	 */
	if( PyArg_ParseTupleAndKeywords(
	     arguments,
	     keywords,
	     "O|",
	     keyword_list,
	     &string_object ) == 0 )
	{
		return( NULL );
	}
	PyErr_Clear();

	result = PyObject_IsInstance(
	          string_object,
	          (PyObject *) &PyUnicode_Type );

	if( result == -1 )
	{
		pyevt_error_fetch_and_raise(
	         PyExc_RuntimeError,
		 "%s: unable to determine if string object is of type Unicode.",
		 function );

		return( NULL );
	}
	else if( result != 0 )
	{
		PyErr_Clear();

#if defined( HAVE_WIDE_SYSTEM_CHARACTER )
		filename_wide = (wchar_t *) PyUnicode_AsUnicode(
		                             string_object );
		Py_BEGIN_ALLOW_THREADS

		result = libevt_check_file_signature_wide(
		          filename_wide,
		          &error );

		Py_END_ALLOW_THREADS
#else
		utf8_string_object = PyUnicode_AsUTF8String(
		                      string_object );

		if( utf8_string_object == NULL )
		{
			pyevt_error_fetch_and_raise(
			 PyExc_RuntimeError,
			 "%s: unable to convert Unicode string to UTF-8.",
			 function );

			return( NULL );
		}
#if PY_MAJOR_VERSION >= 3
		filename_narrow = PyBytes_AsString(
				   utf8_string_object );
#else
		filename_narrow = PyString_AsString(
				   utf8_string_object );
#endif
		Py_BEGIN_ALLOW_THREADS

		result = libevt_check_file_signature(
		          filename_narrow,
		          &error );

		Py_END_ALLOW_THREADS

		Py_DecRef(
		 utf8_string_object );

#endif /* defined( HAVE_WIDE_SYSTEM_CHARACTER ) */

		if( result == -1 )
		{
			pyevt_error_raise(
			 error,
			 PyExc_IOError,
			 "%s: unable to check file signature.",
			 function );

			libcerror_error_free(
			 &error );

			return( NULL );
		}
		if( result != 0 )
		{
			Py_IncRef(
			 (PyObject *) Py_True );

			return( Py_True );
		}
		Py_IncRef(
		 (PyObject *) Py_False );

		return( Py_False );
	}
	PyErr_Clear();

#if PY_MAJOR_VERSION >= 3
	result = PyObject_IsInstance(
		  string_object,
		  (PyObject *) &PyBytes_Type );
#else
	result = PyObject_IsInstance(
		  string_object,
		  (PyObject *) &PyString_Type );
#endif
	if( result == -1 )
	{
		pyevt_error_fetch_and_raise(
	         PyExc_RuntimeError,
		 "%s: unable to determine if string object is of type string.",
		 function );

		return( NULL );
	}
	else if( result != 0 )
	{
		PyErr_Clear();

#if PY_MAJOR_VERSION >= 3
		filename_narrow = PyBytes_AsString(
				   string_object );
#else
		filename_narrow = PyString_AsString(
				   string_object );
#endif
		Py_BEGIN_ALLOW_THREADS

		result = libevt_check_file_signature(
		          filename_narrow,
		          &error );

		Py_END_ALLOW_THREADS

		if( result == -1 )
		{
			pyevt_error_raise(
			 error,
			 PyExc_IOError,
			 "%s: unable to check file signature.",
			 function );

			libcerror_error_free(
			 &error );

			return( NULL );
		}
		if( result != 0 )
		{
			Py_IncRef(
			 (PyObject *) Py_True );

			return( Py_True );
		}
		Py_IncRef(
		 (PyObject *) Py_False );

		return( Py_False );
	}
	PyErr_Format(
	 PyExc_TypeError,
	 "%s: unsupported string object type.",
	 function );

	return( NULL );
}

/* Checks if a file has a Windows Event Log (EVT) file signature using a file-like object
 * Returns a Python object if successful or NULL on error
 */
PyObject *pyevt_check_file_signature_file_object(
           PyObject *self PYEVT_ATTRIBUTE_UNUSED,
           PyObject *arguments,
           PyObject *keywords )
{
	libcerror_error_t *error         = NULL;
	libbfio_handle_t *file_io_handle = NULL;
	PyObject *file_object            = NULL;
	static char *function            = "pyevt_check_file_signature_file_object";
	static char *keyword_list[]      = { "file_object", NULL };
	int result                       = 0;

	PYEVT_UNREFERENCED_PARAMETER( self )

	if( PyArg_ParseTupleAndKeywords(
	     arguments,
	     keywords,
	     "|O",
	     keyword_list,
	     &file_object ) == 0 )
	{
		return( NULL );
	}
	if( pyevt_file_object_initialize(
	     &file_io_handle,
	     file_object,
	     &error ) != 1 )
	{
		pyevt_error_raise(
		 error,
		 PyExc_MemoryError,
		 "%s: unable to initialize file IO handle.",
		 function );

		libcerror_error_free(
		 &error );

		goto on_error;
	}
	Py_BEGIN_ALLOW_THREADS

	result = libevt_check_file_signature_file_io_handle(
	          file_io_handle,
	          &error );

	Py_END_ALLOW_THREADS

	if( result == -1 )
	{
		pyevt_error_raise(
		 error,
		 PyExc_IOError,
		 "%s: unable to check file signature.",
		 function );

		libcerror_error_free(
		 &error );

		goto on_error;
	}
	if( libbfio_handle_free(
	     &file_io_handle,
	     &error ) != 1 )
	{
		pyevt_error_raise(
		 error,
		 PyExc_MemoryError,
		 "%s: unable to free file IO handle.",
		 function );

		libcerror_error_free(
		 &error );

		goto on_error;
	}
	if( result != 0 )
	{
		Py_IncRef(
		 (PyObject *) Py_True );

		return( Py_True );
	}
	Py_IncRef(
	 (PyObject *) Py_False );

	return( Py_False );

on_error:
	if( file_io_handle != NULL )
	{
		libbfio_handle_free(
		 &file_io_handle,
		 NULL );
	}
	return( NULL );
}

/* Creates a new file object and opens it
 * Returns a Python object if successful or NULL on error
 */
PyObject *pyevt_open_new_file(
           PyObject *self PYEVT_ATTRIBUTE_UNUSED,
           PyObject *arguments,
           PyObject *keywords )
{
	pyevt_file_t *pyevt_file = NULL;
	static char *function    = "pyevt_open_new_file";

	PYEVT_UNREFERENCED_PARAMETER( self )

	/* PyObject_New does not invoke tp_init
	 */
	pyevt_file = PyObject_New(
	              struct pyevt_file,
	              &pyevt_file_type_object );

	if( pyevt_file == NULL )
	{
		PyErr_Format(
		 PyExc_MemoryError,
		 "%s: unable to create file.",
		 function );

		goto on_error;
	}
	if( pyevt_file_init(
	     pyevt_file ) != 0 )
	{
		goto on_error;
	}
	if( pyevt_file_open(
	     pyevt_file,
	     arguments,
	     keywords ) == NULL )
	{
		goto on_error;
	}
	return( (PyObject *) pyevt_file );

on_error:
	if( pyevt_file != NULL )
	{
		Py_DecRef(
		 (PyObject *) pyevt_file );
	}
	return( NULL );
}

/* Creates a new file object and opens it using a file-like object
 * Returns a Python object if successful or NULL on error
 */
PyObject *pyevt_open_new_file_with_file_object(
           PyObject *self PYEVT_ATTRIBUTE_UNUSED,
           PyObject *arguments,
           PyObject *keywords )
{
	pyevt_file_t *pyevt_file = NULL;
	static char *function    = "pyevt_open_new_file_with_file_object";

	PYEVT_UNREFERENCED_PARAMETER( self )

	/* PyObject_New does not invoke tp_init
	 */
	pyevt_file = PyObject_New(
	              struct pyevt_file,
	              &pyevt_file_type_object );

	if( pyevt_file == NULL )
	{
		PyErr_Format(
		 PyExc_MemoryError,
		 "%s: unable to create file.",
		 function );

		goto on_error;
	}
	if( pyevt_file_init(
	     pyevt_file ) != 0 )
	{
		goto on_error;
	}
	if( pyevt_file_open_file_object(
	     pyevt_file,
	     arguments,
	     keywords ) == NULL )
	{
		goto on_error;
	}
	return( (PyObject *) pyevt_file );

on_error:
	if( pyevt_file != NULL )
	{
		Py_DecRef(
		 (PyObject *) pyevt_file );
	}
	return( NULL );
}

#if PY_MAJOR_VERSION >= 3

/* The pyevt module definition
 */
PyModuleDef pyevt_module_definition = {
	PyModuleDef_HEAD_INIT,

	/* m_name */
	"pyevt",
	/* m_doc */
	"Python libevt module (pyevt).",
	/* m_size */
	-1,
	/* m_methods */
	pyevt_module_methods,
	/* m_reload */
	NULL,
	/* m_traverse */
	NULL,
	/* m_clear */
	NULL,
	/* m_free */
	NULL,
};

#endif /* PY_MAJOR_VERSION >= 3 */

/* Initializes the pyevt module
 */
#if PY_MAJOR_VERSION >= 3
PyMODINIT_FUNC PyInit_pyevt(
                void )
#else
PyMODINIT_FUNC initpyevt(
                void )
#endif
{
	PyObject *module           = NULL;
	PyGILState_STATE gil_state = 0;

#if defined( HAVE_DEBUG_OUTPUT )
	libevt_notify_set_stream(
	 stderr,
	 NULL );
	libevt_notify_set_verbose(
	 1 );
#endif

	/* Create the module
	 * This function must be called before grabbing the GIL
	 * otherwise the module will segfault on a version mismatch
	 */
#if PY_MAJOR_VERSION >= 3
	module = PyModule_Create(
	          &pyevt_module_definition );
#else
	module = Py_InitModule3(
	          "pyevt",
	          pyevt_module_methods,
	          "Python libevt module (pyevt)." );
#endif
	if( module == NULL )
	{
#if PY_MAJOR_VERSION >= 3
		return( NULL );
#else
		return;
#endif
	}
	PyEval_InitThreads();

	gil_state = PyGILState_Ensure();

	/* Setup the event_types type object
	 */
	pyevt_event_types_type_object.tp_new = PyType_GenericNew;

	if( pyevt_event_types_init_type(
	     &pyevt_event_types_type_object ) != 1 )
	{
		goto on_error;
	}
	if( PyType_Ready(
	     &pyevt_event_types_type_object ) < 0 )
	{
		goto on_error;
	}
	Py_IncRef(
	 (PyObject *) &pyevt_event_types_type_object );

	PyModule_AddObject(
	 module,
	 "event_types",
	 (PyObject *) &pyevt_event_types_type_object );

	/* Setup the file type object
	 */
	pyevt_file_type_object.tp_new = PyType_GenericNew;

	if( PyType_Ready(
	     &pyevt_file_type_object ) < 0 )
	{
		goto on_error;
	}
	Py_IncRef(
	 (PyObject *) &pyevt_file_type_object );

	PyModule_AddObject(
	 module,
	 "file",
	 (PyObject *) &pyevt_file_type_object );

	/* Setup the file_flags type object
	 */
	pyevt_file_flags_type_object.tp_new = PyType_GenericNew;

	if( pyevt_file_flags_init_type(
	     &pyevt_file_flags_type_object ) != 1 )
	{
		goto on_error;
	}
	if( PyType_Ready(
	     &pyevt_file_flags_type_object ) < 0 )
	{
		goto on_error;
	}
	Py_IncRef(
	 (PyObject *) &pyevt_file_flags_type_object );

	PyModule_AddObject(
	 module,
	 "file_flags",
	 (PyObject *) &pyevt_file_flags_type_object );

	/* Setup the record type object
	 */
	pyevt_record_type_object.tp_new = PyType_GenericNew;

	if( PyType_Ready(
	     &pyevt_record_type_object ) < 0 )
	{
		goto on_error;
	}
	Py_IncRef(
	 (PyObject *) &pyevt_record_type_object );

	PyModule_AddObject(
	 module,
	 "record",
	 (PyObject *) &pyevt_record_type_object );

	/* Setup the records type object
	 */
	pyevt_records_type_object.tp_new = PyType_GenericNew;

	if( PyType_Ready(
	     &pyevt_records_type_object ) < 0 )
	{
		goto on_error;
	}
	Py_IncRef(
	 (PyObject *) &pyevt_records_type_object );

	PyModule_AddObject(
	 module,
	 "records",
	 (PyObject *) &pyevt_records_type_object );

	/* Setup the strings type object
	 */
	pyevt_strings_type_object.tp_new = PyType_GenericNew;

	if( PyType_Ready(
	     &pyevt_strings_type_object ) < 0 )
	{
		goto on_error;
	}
	Py_IncRef(
	 (PyObject *) &pyevt_strings_type_object );

	PyModule_AddObject(
	 module,
	 "strings",
	 (PyObject *) &pyevt_strings_type_object );

	PyGILState_Release(
	 gil_state );

#if PY_MAJOR_VERSION >= 3
	return( module );
#else
	return;
#endif

on_error:
	PyGILState_Release(
	 gil_state );

#if PY_MAJOR_VERSION >= 3
	return( NULL );
#else
	return;
#endif
}

