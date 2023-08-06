/*
 * Python object definition of the sequence and iterator object of strings
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

#if !defined( _PYEVT_STRINGS_H )
#define _PYEVT_STRINGS_H

#include <common.h>
#include <types.h>

#include "pyevt_libevt.h"
#include "pyevt_python.h"

#if defined( __cplusplus )
extern "C" {
#endif

typedef struct pyevt_strings pyevt_strings_t;

struct pyevt_strings
{
	/* Python object initialization
	 */
	PyObject_HEAD

	/* The parent object
	 */
	PyObject *parent_object;

	/* The get item by index callback function
	 */
	PyObject* (*get_item_by_index)(
	             PyObject *parent_object,
	             int index );

	/* The current index
	 */
	int current_index;

	/* The number of items
	 */
	int number_of_items;
};

extern PyTypeObject pyevt_strings_type_object;

PyObject *pyevt_strings_new(
           PyObject *parent_object,
           PyObject* (*get_item_by_index)(
                        PyObject *parent_object,
                        int index ),
           int number_of_items );

int pyevt_strings_init(
     pyevt_strings_t *sequence_object );

void pyevt_strings_free(
      pyevt_strings_t *sequence_object );

Py_ssize_t pyevt_strings_len(
            pyevt_strings_t *sequence_object );

PyObject *pyevt_strings_getitem(
           pyevt_strings_t *sequence_object,
           Py_ssize_t item_index );

PyObject *pyevt_strings_iter(
           pyevt_strings_t *sequence_object );

PyObject *pyevt_strings_iternext(
           pyevt_strings_t *sequence_object );

#if defined( __cplusplus )
}
#endif

#endif /* !defined( _PYEVT_STRINGS_H ) */

