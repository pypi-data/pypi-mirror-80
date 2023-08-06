// Python BIP39 Bindings
//
// Copyright 2018-2020 Stichting Polkascan (Polkascan Foundation).
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
// http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

//! Python bindings for the tiny-bip39 crate
//!
//! py-bip39-bindings provides bindings to the Rust create
//! [tiny-bip39](https://crates.io/crates/tiny-bip39), allowing mnemonic generation, validation and
//! conversion to seed and mini-secret.

use pyo3::exceptions;
use pyo3::prelude::*;
use pyo3::{wrap_pyfunction};

use bip39::{Mnemonic, Language, MnemonicType, Seed};
use hmac::Hmac;
use pbkdf2::pbkdf2;
use sha2::Sha512;

/// Create a mini-secret from a BIP39 phrase
///
/// # Arguments
///
/// * `phrase` - Mnemonic phrase
/// * `password` - Use empty string for no password
///
/// # Returns
///
/// Returns the 32-bytes mini-secret via entropy
#[pyfunction]
#[text_signature = "(phrase, password)"]
pub fn bip39_to_mini_secret(phrase: &str, password: &str) -> PyResult<Vec<u8>> {
	let salt = format!("mnemonic{}", password);
	let mnemonic = match Mnemonic::from_phrase(phrase, Language::English) {
		Ok(some_mnemomic) => some_mnemomic,
		Err(err) => return Err(exceptions::ValueError::py_err(format!("Invalid mnemonic: {}", err.to_string())))
	};
	let mut result = [0u8; 64];

	pbkdf2::<Hmac<Sha512>>(mnemonic.entropy(), salt.as_bytes(), 2048, &mut result);

	Ok(result[..32].to_vec())
}

/// Generates a new mnemonic
///
/// # Arguments
///
/// * `words` - The amount of words to generate, valid values are 12, 15, 18, 21 and 24
///
/// # Returns
///
/// A string containing the mnemonic words.
#[pyfunction]
#[text_signature = "(words)"]
pub fn bip39_generate(words: u32) -> PyResult<String> {

	let word_count_type = match MnemonicType::for_word_count(words as usize) {
		Ok(some_work_count) => some_work_count,
		Err(err) => return Err(exceptions::ValueError::py_err(err.to_string()))
	};

	let phrase = Mnemonic::new(word_count_type, Language::English).into_phrase();

	assert_eq!(phrase.split(" ").count(), words as usize);

	Ok(phrase.to_owned())
}

/// Creates a seed from a BIP39 phrase
///
/// # Arguments
///
/// * `phrase` - Mnemonic phrase
/// * `password` - Use empty string for no password
///
/// # Returns
///
/// Returns a 32-bytes seed
#[pyfunction]
#[text_signature = "(phrase, password)"]
pub fn bip39_to_seed(phrase: &str, password: &str) -> PyResult<Vec<u8>> {
	let mnemonic = match Mnemonic::from_phrase(phrase, Language::English) {
		Ok(some_mnemomic) => some_mnemomic,
		Err(err) => return Err(exceptions::ValueError::py_err(format!("Invalid mnemonic: {}", err.to_string())))
	};

	Ok(Seed::new(&mnemonic, password)
		.as_bytes()[..32]
		.to_vec())
}


/// Validates a BIP39 phrase
///
/// # Arguments
///
/// * `phrase` - Mnemonic phrase
///
/// # Returns
///
/// Returns boolean with validation result
#[pyfunction]
#[text_signature = "(phrase)"]
pub fn bip39_validate(phrase: &str) -> bool {
	match Mnemonic::validate(phrase, Language::English) {
		Err(_) => false,
		_ => true
	}
}

#[pymodule]
fn bip39(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_wrapped(wrap_pyfunction!(bip39_to_mini_secret))?;
	m.add_wrapped(wrap_pyfunction!(bip39_generate))?;
	m.add_wrapped(wrap_pyfunction!(bip39_to_seed))?;
	m.add_wrapped(wrap_pyfunction!(bip39_validate))?;
    Ok(())
}
